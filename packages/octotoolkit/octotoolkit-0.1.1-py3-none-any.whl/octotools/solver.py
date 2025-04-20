import os
import sys
import json
import argparse
import time
from typing import Optional

from octotools.models.initializer import Initializer
from octotools.models.planner import Planner
from octotools.models.memory import Memory
from octotools.models.executor import Executor
from octotools.models.utils import make_json_serializable_truncated

class Solver:
    def __init__(
        self,
        planner,
        memory,
        executor,
        output_types: str = "base,final,direct",
        max_steps: int = 10,
        max_time: int = 300,
        max_tokens: int = 4000,
        root_cache_dir: str = "cache"
    ):
        self.planner = planner
        self.memory = memory
        self.executor = executor
        self.max_steps = max_steps
        self.max_time = max_time
        self.max_tokens = max_tokens
        self.root_cache_dir = root_cache_dir

        self.output_types = output_types.lower().split(',')
        assert all(output_type in ["base", "final", "direct"] for output_type in self.output_types), "Invalid output type. Supported types are 'base', 'final', 'direct'."

    def solve(self, question: str, image_path: Optional[str] = None):
        """
        Solve a single problem from the benchmark dataset.
        
        Args:
            index (int): Index of the problem to solve
        """
        # Update cache directory for the executor
        self.executor.set_query_cache_dir(self.root_cache_dir)

        # Initialize json_data with basic problem information
        json_data = {
            "query": question,
            "image": image_path
        }

        # Generate base response if requested
        if 'base' in self.output_types:
            base_response = self.planner.generate_base_response(question, image_path, self.max_tokens)
            json_data["base_response"] = base_response

        # If only base response is needed, save and return
        if set(self.output_types) == {'base'}:
            return json_data
    
        # Continue with query analysis and tool execution if final or direct responses are needed
        if {'final', 'direct'} & set(self.output_types):

             # Analyze query
            query_analysis = self.planner.analyze_query(question, image_path)
            json_data["query_analysis"] = query_analysis

            start_time = time.time()
            step_count = 0
            action_times = []

            # Main execution loop
            while step_count < self.max_steps and (time.time() - start_time) < self.max_time:
                step_count += 1

                # Generate next step
                start_time_step = time.time()
                next_step = self.planner.generate_next_step(
                    question, 
                    image_path, 
                    query_analysis, 
                    self.memory, 
                    step_count, 
                    self.max_steps
                )
                context, sub_goal, tool_name = self.planner.extract_context_subgoal_and_tool(next_step)


                if tool_name is None or tool_name not in self.planner.available_tools:
                    print(f"Error: Tool '{tool_name}' is not available or not found.")
                    command = "Not command is generated due to the tool not found."
                    result = "Not result is generated due to the tool not found."

                else:
                    # Generate the tool command
                    tool_command = self.executor.generate_tool_command(
                        question, 
                        image_path, 
                        context, 
                        sub_goal, 
                        tool_name, 
                        self.planner.toolbox_metadata[tool_name]
                    )
                    explanation, command = self.executor.extract_explanation_and_command(tool_command)
                    

                    # Execute the tool command
                    result = self.executor.execute_tool_command(tool_name, command)
                    print("!!! type of result: ", type(result))

                    result = make_json_serializable_truncated(result) # Convert to JSON serializable format


                # Track execution time
                end_time_step = time.time()
                execution_time_step = round(end_time_step - start_time_step, 2)
                action_times.append(execution_time_step)

                # Update memory
                self.memory.add_action(step_count, tool_name, sub_goal, command, result)
                memeory_actions = self.memory.get_actions()

                # Verify memory
                stop_verification = self.planner.verificate_context(
                    question, 
                    image_path, 
                    query_analysis, 
                    self.memory
                )
                conclusion = self.planner.extract_conclusion(stop_verification)
                

                if conclusion == 'STOP':
                    break


            # Add memory and statistics to json_data
            json_data.update({
                "memory": memeory_actions,
                "step_count": step_count,
                "execution_time": round(time.time() - start_time, 2),
            })

            # Generate final output if requested
            if 'final' in self.output_types:
                final_output = self.planner.generate_final_output(question, image_path, self.memory)
                json_data["final_output"] = final_output

            # Generate direct output if requested
            if 'direct' in self.output_types:
                direct_output = self.planner.generate_direct_output(question, image_path, self.memory)
                json_data["direct_output"] = direct_output

        return json_data
            
def parse_arguments():
    parser = argparse.ArgumentParser(description="Run the octotools demo with specified parameters.")
    parser.add_argument("--llm_engine_name", default="gpt-4o", help="LLM engine name.")
    parser.add_argument(
        "--output_types",
        default="base,final,direct",
        help="Comma-separated list of required outputs (base,final,direct)"
    )
    parser.add_argument("--enabled_tools", default="Generalist_Solution_Generator_Tool", help="List of enabled tools.")
    parser.add_argument("--root_cache_dir", default="solver_cache", help="Path to solver cache directory.")
    parser.add_argument("--max_tokens", type=int, default=4000, help="Maximum tokens for LLM generation.")
    parser.add_argument("--max_steps", type=int, default=10, help="Maximum number of steps to execute.")
    parser.add_argument("--max_time", type=int, default=300, help="Maximum time allowed in seconds.")
    parser.add_argument("--verbose", type=bool, default=True, help="Enable verbose output.")
    return parser.parse_args()

def construct_solver(llm_engine_name : str = "gpt-4o",
                     enabled_tools : list[str] = ["all"],
                     output_types : str = "direct",
                     max_steps : int = 10,
                     max_time : int = 300,
                     max_tokens : int = 4000,
                     root_cache_dir : str = "solver_cache"
                     ):
    # Instantiate Initializer
    initializer = Initializer(
        enabled_tools=enabled_tools,
        model_string=llm_engine_name
    )

    # Instantiate Planner
    planner = Planner(
        llm_engine_name=llm_engine_name,
        toolbox_metadata=initializer.toolbox_metadata,
        available_tools=initializer.available_tools,
    )

    # Instantiate Memory
    memory = Memory()

    # Instantiate Executor
    executor = Executor(
        llm_engine_name=llm_engine_name,
        root_cache_dir=root_cache_dir
    )


    # Instantiate Solver
    solver = Solver(
        planner=planner,
        memory=memory,
        executor=executor,
        output_types=output_types,
        max_steps=max_steps,
        max_time=max_time,
        max_tokens=max_tokens,
        root_cache_dir=root_cache_dir
    )

    return solver

def main(args):
    solver = construct_solver(llm_engine_name=args.llm_engine_name, 
                              enabled_tools=args.enabled_tools, 
                              output_types=args.output_types, 
                              max_steps=args.max_steps, 
                              max_time=args.max_time, 
                              max_tokens=args.max_tokens, 
                              root_cache_dir=args.root_cache_dir)
    # Solve the task or problem
    solver.solve("What is the capital of France?")

if __name__ == "__main__":
    args = parse_arguments()
    main(args)
