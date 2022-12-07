from functools import lru_cache

from pydantic import BaseSettings


class Settings(BaseSettings):
    db_path: str = "backend.sqlite3"


@lru_cache()
def get_settings() -> Settings:
    return Settings()
