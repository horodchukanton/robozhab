from functools import lru_cache

from pydantic import BaseSettings


@lru_cache
def get_settings():
    return Settings()


class Settings(BaseSettings):
    api_id: str
    api_hash: str
    chat_id: int = None
    invite_hash: str = None
    timezone: int = +3

    class Config:
        case_sensitive = True
        env_file = '.env'
        env_file_encoding = 'utf-8'
