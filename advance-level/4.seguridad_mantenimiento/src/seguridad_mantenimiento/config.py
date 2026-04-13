"""
Application configuration using pydantic-settings.

Values are loaded in this priority order (highest → lowest):
    1. Real environment variables
    2. .env file (if present)
    3. Default values defined here

Secrets use SecretStr so they are never printed in logs or tracebacks.
"""

from pydantic import SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # General application settings
    app_name: str = "seguridad-mantenimiento"
    debug: bool = False
    port: int = 8000

    # Connection settings
    database_url: str = "sqlite:///./app.db"

    # Sensitive value — stored as SecretStr, never exposed in repr/str
    api_key: SecretStr = SecretStr("changeme")


def get_settings() -> Settings:
    """Return a Settings instance loaded from the environment."""
    return Settings()
