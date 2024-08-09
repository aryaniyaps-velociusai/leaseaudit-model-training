from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    azure_openai_api_key: SecretStr

    azure_openai_endpoint: str

    azure_openai_api_version: str

    azure_openai_deployment: str

    azure_openai_model: str

    azure_document_intelligence_key: SecretStr

    azure_document_intelligence_endpoint: str

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()  # type: ignore[call-args]
