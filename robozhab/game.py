from datetime import timedelta, datetime

from robozhab.base.chat import Chat
from robozhab.base.settings import Settings
from robozhab.base.tg_client import APIClient
from robozhab.game.info import ZhabaInfo


class Game(Chat):
    settings: Settings = None

    def __init__(self, client: APIClient, settings: Settings):
        chat_id = super().resolve_chat_id(settings.chat_id)
        super().__init__(client, chat_id)
        self.settings = settings

    def schedule(self):
        # Check if we have scheduled messages pending

        # Check if is available to run now

        schedule_start = datetime.now(tz=self.settings.tz)

        for i in range(self.settings.schedule_days):
            date = schedule_start + timedelta(days=i)

            if self.settings.feed_freq:
                self.schedule_daily_feed(date)

            if self.settings.work_freq:
                self.schedule_daily_work(date)

            if self.settings.has_a_child:
                self.schedule_daily_child_feed(date)

    def schedule_daily_feed(self, date: datetime):
        feed_text = self.settings.feed_text
        for i in range(0, 24, self.settings.feed_freq):
            feed_time = date + timedelta(hours=i, minutes=0)
            self.schedule_message(feed_text, feed_time)

    def schedule_daily_work(self, date: datetime):
        work_text = self.settings.work_text
        finish_work_text = "Завершить работу"

        for i in range(0, 24, self.settings.work_freq):
            work_time = date + timedelta(hours=i, minutes=0)
            self.schedule_message(work_text, work_time)

            finish_time = work_time + timedelta(hours=2, minutes=1)
            self.schedule_message(finish_work_text, finish_time)

            if self.settings.work_reanimate:
                reanimate_time = finish_time + timedelta(seconds=5)
                self.schedule_message("Реанимировать жабу", reanimate_time)

    def schedule_daily_child_feed(self, date: datetime):
        feed_child_text = "Покормить жабёнка"
        for i in range(0, 24, 12):
            feed_child_time = date + timedelta(hours=i, minutes=0)
            self.schedule_message(feed_child_text, feed_child_time)


class FeedLoop:
    available_in: int = None
    feed_period = 8 * 60
    premium_feed_period = 6 * 60
    overfeed_period = 4 * 60

    def __init__(self, settings: Settings, info: ZhabaInfo):
        self._info = info
        self.settings = settings

    def next_available_datetime(self):
        pass

    def is_available_now(self):
        if self.settings.feed_text.lower() == "Покормить жабу":
            return not self._info.feed_in_minutes
        elif self.settings.feed_text.lower() == "Откормить жабу":
            return not self._info.overfeed_in_minutes
        return None

    def next_available(self, date=None):
        if not date and self.is_available_now:
            return datetime.now(tz=self.settings.tz)
