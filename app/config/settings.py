from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="UTF-8"
    )

    # GUNICORN
    gunicorn_port: str
    gunicorn_workers: str


@lru_cache
def get_settings() -> Settings:
    return Settings()