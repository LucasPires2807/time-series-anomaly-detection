from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="UTF-8"
    )

    # GUNICORN
    gunicorn_port: str
    gunicorn_workers: str

    # DATABASE
    driver: str
    dialect: str
    db_user: str
    db_password: str
    db_host: str
    db_port: str
    db_name: str
    postgres_password: str
    postgres_db: str

    @property
    def database_url(self) -> str:
        return (
            f"{self.dialect}+{self.driver}://{self.db_user}:{self.db_password}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


@lru_cache
def get_settings() -> Settings:
    return Settings()