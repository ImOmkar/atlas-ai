from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Atlas AI"
    app_version: str = "0.1.0"

    debug: bool = False

    host: str = "127.0.0.1"
    port: int = 8000

    database_url: str

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    gemini_api_key: str = "your_api_key"

    gemini_chat_model: str = "gemini-3.5-flash"

    gemini_embedding_model: str = "gemini-embedding-001"

    secret_key: str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()