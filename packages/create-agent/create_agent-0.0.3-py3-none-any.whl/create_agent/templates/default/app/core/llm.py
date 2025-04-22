from app.config import settings
from app.utils.logging import logger
from langchain_openai import ChatOpenAI


class LLMManager:
    _instances = {}

    def __new__(cls, model_name: str = None):
        # Ensure we have a valid model name
        model_name = model_name or settings.LLM_MODEL

        # Create a separate instance for each model
        if model_name not in cls._instances:
            instance = super(LLMManager, cls).__new__(cls)
            instance._llm = None
            instance._model_name = model_name
            cls._instances[model_name] = instance
        return cls._instances[model_name]

    @property
    def llm(self):
        if self._llm is None:
            logger.info(f"Initializing LLM: {self._model_name}")
            self._llm = ChatOpenAI(model=self._model_name)
            self._llm.model_kwargs = {
                "temperature": settings.LLM_TEMPERATURE,
                "top_p": settings.LLM_TOP_P,
                "frequency_penalty": settings.LLM_FREQUENCY_PENALTY,
                "presence_penalty": settings.LLM_PRESENCE_PENALTY,
                "max_tokens": settings.LLM_MAX_TOKENS,
            }
        return self._llm


def get_llm(model_name: str = None):
    """Initialize and return the LLM."""
    return LLMManager(model_name).llm
