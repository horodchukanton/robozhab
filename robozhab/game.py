from datetime import timedelta, datetime

from robozhab.base.tg_client import APIClient
from robozhab.base.chat import Chat
from robozhab.base.settings import Settings


class Game(Chat):

    settings: Settings = None

    def __init__(self, client: APIClient, settings: Settings):
        chat_id = super().resolve_chat_id(settings.chat_id)
        super().__init__(client, chat_id)
        self.settings = settings

    @staticmethod
    def get_next_offset():
        # pylint: disable=fixme
        # TODO: This looks ugly AF, there should be a better solution
        with open('.offset', 'r', encoding='UTF-8') as f:
            current = f.readline(-1)
            if current == "":
                current = 0

        result = int(current) + 1

        with open('.offset', 'w', encoding='UTF-8') as f:
            f.write(f"{result}")

        return result

    def schedule_day(self, date: datetime):
        # Normalizing
        date = date.replace(hour=0, minute=0, second=0)

        # The main bot has a lag, so we should set up a one minute offset
        offset = self.get_next_offset()
        date = date + timedelta(minutes=offset)

        # Feed time
        feed_text = self.settings.feed_text
        for i in range(0, 24, self.settings.feed_freq):
            feed_time = date + timedelta(hours=i, minutes=0)
            self.schedule_message(feed_text, feed_time)

        # Work time
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

        if self.settings.has_a_child:
            feed_child_text = "Покормить жабёнка"
            for i in range(0, 24, 12):
                feed_child_time = date + timedelta(hours=i, minutes=0)
                self.schedule_message(feed_child_text, feed_child_time)

    def schedule(self):
        for i in range(self.settings.schedule_days):
            date = datetime.now(tz=self.settings.tz) + timedelta(days=i)
            self.schedule_day(date)
