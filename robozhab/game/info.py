from pydantic import BaseModel


class ZhabaInfo(BaseModel):
    work_start_in: int = None
    work_end_in: int = None

    feed_in_minutes: int = None
    overfeed_in_minutes: int = None


class ChildInfo(BaseModel):
    feed_in: int = None

    kindergarten_available: bool = False
    kindergarten_leave_in: int = None

    fight_available: bool = False
