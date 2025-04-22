import os
from typing import List,Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # App settings
    APP_NAME: str = Field(default="{{ project_title }} API", description="App name")
    APP_VERSION: str = Field(default="1.0.0", description="App version")
    APP_DESCRIPTION: str = Field(
        default="OpenAI-compatible API for {{ project_title }}",
        description="App description",
    )

    # Database settings
    DATABASE_URL: str = Field(default="", description="Database URL")

    # API settings
    API_KEY: str = Field(default="", description="API key for authentication")
    
    # CORS settings
    CORS_ORIGINS: List[str] = Field(default=["*"], description="Allowed CORS origins")

    # LLM settings
    OPENAI_API_KEY: str = Field(default="", description="OpenAI API key")
    LLM_MODEL: str = Field(
        default="gpt-4o-mini-2024-07-18",
        description="Main LLM model to use",
    )
    LLM_TEMPERATURE: float | None = Field(
        default=0, description="LLM temperature parameter"
    )
    LLM_TOP_P: float | None = Field(default=0.1, description="LLM top-p parameter")
    LLM_FREQUENCY_PENALTY: float | None = Field(
        default=0.1, description="LLM frequency penalty"
    )
    LLM_PRESENCE_PENALTY: float | None = Field(
        default=0.1, description="LLM presence penalty"
    )
    LLM_MAX_TOKENS: int | None = Field(
        default=3000, description="Maximum tokens for LLM"
    )

    # System settings
    DEBUG: Optional[bool] = Field(default=False, description="Debug mode")
    LOG_LEVEL: str = Field(
        default="INFO",
        pattern="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$",
        description="Logging level",
    )

    # Tracing settings
    LANGSMITH_API_KEY: str = Field(default="", description="Langsmith API key")
    LANGSMITH_TRACING: str = Field(default="true", description="Langsmith tracing")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="allow",
    )

    @field_validator("DATABASE_URL")
    def validate_database_url(cls, v):
        if not v:
            raise ValueError("DATABASE_URL is required")
        return v

    @field_validator("API_KEY")
    def validate_api_key(cls, v):
        if not v:
            raise ValueError("API_KEY is required")
        return v

    @field_validator("LOG_LEVEL")
    def validate_log_level(cls, v: str) -> str:
        if not v:
            return "INFO"
        level = v.upper()
        valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if level not in valid_levels:
            return "INFO"
        return level

    def setup_env(self):
        """Setup environment variables."""
        if "OPENAI_API_KEY" in os.environ:
            del os.environ["OPENAI_API_KEY"]
        os.environ["OPENAI_API_KEY"] = self.OPENAI_API_KEY
        if "LANGSMITH_API_KEY" in os.environ:
            del os.environ["LANGSMITH_API_KEY"]
        os.environ["LANGSMITH_API_KEY"] = self.LANGSMITH_API_KEY
        if "LANGSMITH_TRACING" in os.environ:
            del os.environ["LANGSMITH_TRACING"]
        os.environ["LANGSMITH_TRACING"] = self.LANGSMITH_TRACING


settings = Settings()
settings.setup_env() 