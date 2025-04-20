#%%
import os
import json
from crewai import LLM

class CrewAILLMFactory:
    _model_to_provider = {
        'gpt': 'openai',
        'gpt-4o': 'openai',
        'gpt-4o-mini': 'openai',
        'o1-': 'openai',
        'o3-': 'openai',
        'llama': 'meta',
        'gemini': 'google',
        'claude': 'anthropic',
        'deepseek': 'deepseek',
        'cognitivecomputations/': 'openrouter',
        'google/': 'openrouter',
        'mistralai/': 'openrouter',
        'qwen/': 'openrouter',
        'meta-llama/': 'openrouter',
        'deepseek/': 'openrouter',
        'nvidia/': 'openrouter',
        'microsoft/': 'openrouter'
    }

    @classmethod
    def get_provider(cls, model: str) -> str:
        # Prioritize keys with '/' (more specific)
        sorted_keys = sorted(cls._model_to_provider.keys(), key=lambda x: '/' not in x)
        for key in sorted_keys:
            if key in model:
                return cls._model_to_provider[key]
        raise ValueError(f"Unknown model provider for model: {model}")

    @classmethod
    def create_llm(cls, model: str, **kwargs) -> LLM:
        provider = cls.get_provider(model)

        if provider == 'openai':
            full_model = model if model.startswith("openai/") else f"openai/{model}"
            return LLM(
                model=full_model,
                api_key=os.getenv("OPENAI_API_KEY"),
                **kwargs
            )

        elif provider == 'anthropic':
            full_model = model if model.startswith("anthropic/") else f"anthropic/{model}"
            return LLM(
                model=full_model,
                api_key=os.getenv("ANTHROPIC_API_KEY"),
                **kwargs
            )

        elif provider == 'google':
            if model.startswith("openrouter/"):  # Special case
                full_model = model
                return LLM(
                    model=full_model,
                    api_key=os.getenv("OPENROUTER_API_KEY"),
                    base_url="https://openrouter.ai/api/v1",
                    **kwargs
                )
            else:
                creds_path = os.getenv("GOOGLE_VERTEX_CREDENTIALS_JSON")
                full_model = model if model.startswith("gemini/") else f"gemini/{model}"
                if creds_path:
                    with open(creds_path, 'r') as f:
                        creds_json = json.dumps(json.load(f))
                    return LLM(
                        model=full_model,
                        vertex_credentials=creds_json,
                        **kwargs
                    )
                else:
                    return LLM(
                        model=full_model,
                        api_key=os.getenv("GEMINI_API_KEY"),
                        **kwargs
                    )

        elif provider == 'openrouter':
            full_model = model if model.startswith("openrouter/") else f"openrouter/{model}"
            return LLM(
                model=full_model,
                api_key=os.getenv("OPENROUTER_API_KEY"),
                base_url="https://openrouter.ai/api/v1",
                **kwargs
            )

        else:
            raise NotImplementedError(f"Provider '{provider}' is not yet supported.")
