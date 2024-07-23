import os
from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    web_port: int = 8000
    redis_host: str = "localhost"
    redis_port: str = "6379"
    redis_user: str = ""
    redis_password: str = ""
    database_url: str = "sqlite:///database.db"
    high_threshold: int = 100
    low_threshold: int = 10

    model_config = SettingsConfigDict(env_file=os.path.join(BASE_DIR, ".env"))


@lru_cache
def get_settings() -> Settings:
    return Settings()
