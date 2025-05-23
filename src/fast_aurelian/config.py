from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="FAST_AURELIAN_",
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    api_key: str | None = Field(default=None, description="API key for authentication (optional)")
    host: str = Field(default="0.0.0.0", description="Host to bind the server to")
    port: int = Field(default=8000, description="Port to bind the server to")
    debug: bool = Field(default=False, description="Enable debug mode")

    log_level: str = Field(default="info", description="Logging level")
    log_format: str = Field(
        default="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
        description="Log format string",
    )

    cors_origins: list[str] = Field(
        default_factory=lambda: ["*"], description="CORS allowed origins"
    )
    cors_methods: list[str] = Field(
        default_factory=lambda: ["*"], description="CORS allowed methods"
    )
    cors_headers: list[str] = Field(
        default_factory=lambda: ["*"], description="CORS allowed headers"
    )

    aurelian_workdir: str | None = Field(default=None, description="Aurelian working directory")
    openai_api_key: str | None = Field(default=None, description="OpenAI API key")

    app_name: str = Field(default="Fast-Aurelian", description="Application name")
    app_version: str = Field(default="0.1.0", description="Application version")
    docs_url: str = Field(default="/docs", description="Swagger UI docs URL")
    redoc_url: str = Field(default="/redoc", description="ReDoc docs URL")

    max_concurrent_requests: int = Field(default=10, description="Maximum concurrent requests")
    request_timeout: int = Field(default=300, description="Request timeout in seconds")


@lru_cache
def get_settings() -> Settings:
    """Get application settings with caching for performance."""
    return Settings()
