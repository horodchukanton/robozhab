from datetime import timedelta, datetime
from base.chat import Chat, resolve_chat_id
from base.settings import Settings


class Game(Chat):

    config: Settings = None

    def __init__(self, chat_id, config):
        super().__init__(chat_id)
        self.config = config

    @classmethod
    def from_settings(cls, settings):
        chat_id = resolve_chat_id(settings)
        return Game(chat_id, settings)

    @staticmethod
    def get_next_offset():
        # TODO: This looks ugly AF, there should be a better solution
        with open('.offset', 'r') as f:
            current = f.readline(-1)
            if current == "":
                current = 0

        result = int(current) + 1

        with open('.offset', 'w') as f:
            f.write(f"{result}")

        return result

    def schedule_day(self, date: datetime):
        # Normalizing
        date = date.replace(hour=0, minute=0, second=0)

        # The main bot has a lag, so we should set up a one minute offset
        offset = self.get_next_offset()
        date = date + timedelta(minutes=offset)

        # Feed time
        feed_text = self.config.feed_text
        for i in range(0, 24, self.config.feed_freq):
            feed_time = date + timedelta(hours=i, minutes=0)
            self.schedule_message(feed_text, feed_time)

        # Work time
        work_text = self.config.work_text
        finish_work_text = "Завершить работу"
        for i in range(0, 24, self.config.work_freq):

            work_time = date + timedelta(hours=i, minutes=0)
            self.schedule_message(work_text, work_time)

            finish_time = work_time + timedelta(hours=2, minutes=1)
            self.schedule_message(finish_work_text, finish_time)

            if self.config.work_reanimate:
                reanimate_time = finish_time + timedelta(seconds=5)
                self.schedule_message("Реанимировать жабу", reanimate_time)

        if self.config.has_a_child:
            feed_child_text = "Покормить жабёнка"
            for i in range(0, 24, 12):
                feed_child_time = date + timedelta(hours=i, minutes=0)
                self.schedule_message(feed_child_text, feed_child_time)

    def schedule(self):
        for i in range(self.config.schedule_days):
            date = datetime.now(tz=self.config.tz) + timedelta(days=i)
            self.schedule_day(date)
