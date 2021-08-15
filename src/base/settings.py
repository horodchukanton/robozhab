from functools import lru_cache

from pydantic import BaseSettings
from datetime import timezone, timedelta


@lru_cache(maxsize=1)
def get_settings():
    return Settings()


class Settings(BaseSettings):
    api_id: str
    api_hash: str
    chat_id: int = None
    invite_hash: str = None
    timezone: int = +3

    @property
    def tz(self) -> timezone:
        utcoffset = self.__dict__.get('timezone')
        return timezone(timedelta(hours=utcoffset))

    class Config:
        case_sensitive = True
        env_file = '.env'
        env_file_encoding = 'utf-8'
