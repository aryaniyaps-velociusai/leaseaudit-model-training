from functools import lru_cache
from langchain_core.language_models import BaseChatModel
from langchain_openai import AzureChatOpenAI

from app.core.config import settings


@lru_cache()
def get_chat_model() -> BaseChatModel:
    """Get a chat model instance based on the given chat model type."""
    return AzureChatOpenAI(
        model=settings.azure_openai_model,
        api_key=settings.azure_openai_api_key.get_secret_value(),  # type: ignore[arg-type]
        azure_endpoint=settings.azure_openai_endpoint,
        api_version=settings.azure_openai_api_version,
        azure_deployment=settings.azure_openai_deployment,
        temperature=0.1,
        max_tokens=None,
        timeout=600,
        max_retries=2,
    )
