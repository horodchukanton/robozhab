import datetime
from functools import lru_cache

from pydantic import BaseSettings


@lru_cache(maxsize=1)
def get_settings(filename: str = None):
    if filename:
        return Settings(_env_file=filename)
    return Settings()


class Settings(BaseSettings):
    api_id: int
    api_hash: str
    chat_id: int
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
        case_sensitive = False
        env_file = '.env'
        env_file_encoding = 'utf-8'


class SettingsV2(BaseSettings):
    API_ID: int
    API_HASH: str

    CHAT_ID: int
    TIMEZONE: int = +3

    WORK_TYPE: int = 2  # Столовая, Крупье, Грабитель
    FEED_TYPE: int = 2  # Покормить, Откормить
    HAS_A_CHILD: bool = False
    HAS_A_CLAN: bool = False

    class Config:
        case_sensitive = True
        env_file = '.env'
        env_file_encoding = 'utf-8'

    @classmethod
    def from_v1(cls, settings_v1: Settings):

        feed_type = 0
        if settings_v1.feed_text.lower() == "покормить жабу":
            feed_type = 1
        elif settings_v1.feed_text.lower() == "откормить жабу":
            feed_type = 2

        work_type = 0
        if settings_v1.work_text.lower() == "поход в столовую":
            work_type = 1
        elif settings_v1.work_text.lower() == "работа крупье":
            work_type = 2
        elif settings_v1.work_text.lower() == "работа грабитель":
            work_type = 3

        return SettingsV2(
            API_ID=settings_v1.api_id,
            API_HASH=settings_v1.api_hash,
            CHAT_ID=settings_v1.chat_id,
            TIMEZONE=settings_v1.timezone,
            HAS_A_CHILD=settings_v1.has_a_child,
            HAS_A_CLAN=settings_v1.has_a_clan,
            WORK_TYPE=work_type,
            FEED_TYPE=feed_type,
        )
