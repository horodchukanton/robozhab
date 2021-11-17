from functools import lru_cache

import datetime
from pydantic import BaseSettings


@lru_cache(maxsize=1)
def get_settings(filename: str = None):
    if filename:
        return Settings(_env_file=filename)
    return Settings()


class Settings(BaseSettings):
    api_id: str
    api_hash: str
    chat_id: int = None
    timezone: int = +3

    schedule_days: int = 5
    work_reanimate: bool = False
    work_text: str = "Работа крупье"
    work_freq: int = 8

    feed_text: str = "Покормить жабу"
    feed_freq: int = 12

    has_a_child: bool = False
    has_a_clan: bool = False

    @property
    def tz(self) -> datetime.timezone:
        utcoffset = self.__dict__.get('timezone')
        return datetime.timezone(datetime.timedelta(hours=utcoffset))

    class Config:
        case_sensitive = True
        env_file = '.env'
        env_file_encoding = 'utf-8'
