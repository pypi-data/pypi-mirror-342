from typing import Any

def create_llm_engine(model_string: str, use_cache: bool = False, is_multimodal: bool = True) -> Any:
    """
    Factory function to create appropriate LLM engine instance.
    """
    if any(x in model_string for x in ["gpt", "o1", "o3", "o4"]):
        from .openai import ChatOpenAI
        return ChatOpenAI(model_string=model_string, use_cache=use_cache, is_multimodal=is_multimodal)
    
    elif "claude" in model_string:
        from .anthropic import ChatAnthropic
        return ChatAnthropic(model_string=model_string, use_cache=use_cache, is_multimodal=is_multimodal)
    
    elif any(x in model_string for x in ["deepseek-chat", "deepseek-reasoner"]):
        from .deepseek import ChatDeepseek
        return ChatDeepseek(model_string=model_string, use_cache=use_cache, is_multimodal=is_multimodal)
    
    elif "gemini" in model_string:
        from .gemini import ChatGemini
        return ChatGemini(model_string=model_string, use_cache=use_cache, is_multimodal=is_multimodal)
    
    elif any(x in model_string for x in ["grok"]):
        from .xai import ChatGrok
        return ChatGrok(model_string=model_string, use_cache=use_cache, is_multimodal=is_multimodal)
    
    elif any(x in model_string for x in ["vllm"]):
        # TODO: Check if this is correct
        from .vllm import ChatVLLM
        return ChatVLLM(model_string=model_string, use_cache=use_cache, is_multimodal=is_multimodal)
    
    elif any(x in model_string for x in ["meta-llama", 
                                         "deepseek-ai", 
                                         "mistralai", 
                                         "Qwen", 
                                         "databricks", 
                                         "microsoft", 
                                         "nvidia", 
                                         "google"]):
        # FIXME: Check if this is correct
        from .together import ChatTogether
        return ChatTogether(model_string=model_string, use_cache=use_cache, is_multimodal=is_multimodal)
    else:
        try:
            from .together import ChatTogether
            return ChatTogether(model_string=model_string, use_cache=use_cache, is_multimodal=is_multimodal)
        except:
            raise ValueError(f"Unknown LLM engine: {model_string}")

