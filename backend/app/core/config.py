"""
Core configuration using Pydantic Settings.
All environment variables are validated and accessible through the `settings` object.
"""

from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = Field(default="Agentic Loan Underwriter", alias="APP_NAME")
    app_version: str = Field(default="0.1.0", alias="APP_VERSION")
    debug: bool = Field(default=False, alias="DEBUG")
    environment: str = Field(default="development", alias="ENVIRONMENT")
    api_v1_prefix: str = Field(default="/api/v1", alias="API_V1_PREFIX")

    # Server
    host: str = Field(default="0.0.0.0", alias="HOST")
    port: int = Field(default=8000, alias="PORT")

    # Database
    database_url: Optional[str] = Field(default=None, alias="DATABASE_URL")

    # OpenAI
    openai_api_key: str = Field(..., alias="OPENAI_API_KEY")

    # LiteLLM Proxy
    litellm_endpoint: str = Field(
        default="http://localhost:4000", alias="LITELLM_ENDPOINT")

    # LangSmith (Observability)
    langsmith_api_key: Optional[str] = Field(
        default=None, alias="LANGSMITH_API_KEY")
    langsmith_project: str = Field(
        default="agentic-loan-underwriter", alias="LANGSMITH_PROJECT")

    @property
    def is_development(self) -> bool:
        return self.environment == "development"

    @property
    def is_production(self) -> bool:
        return self.environment == "production"


# Singleton instance
settings = Settings()
