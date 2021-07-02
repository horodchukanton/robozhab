from datetime import timedelta, datetime

from src.base.chat import Chat, resolve_chat_id


def from_settings(settings):
    chat_id = resolve_chat_id(settings)
    return Game(chat_id)


class Game(Chat):

    def get_next_offset(self):
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

        # Feed time ( Every 12 hours )
        feed_text = "Покормить жабу"
        first_feed = date + timedelta(hours=0, minutes=0)
        second_feed = date + timedelta(hours=12, minutes=0)
        self.schedule_message(feed_text, first_feed)
        self.schedule_message(feed_text, second_feed)

        # Work time ( Every 6 hours )
        work_text = "Работа крупье"
        first_work = date + timedelta(hours=0, minutes=0)
        second_work = date + timedelta(hours=8, minutes=0)
        third_work = date + timedelta(hours=16, minutes=0)
        self.schedule_message(work_text, first_work)
        self.schedule_message(work_text, second_work)
        self.schedule_message(work_text, third_work)

        # Finish work ( 2 hours after work )
        finish_work_text = "Завершить работу"
        first_work_end = date + timedelta(hours=2, minutes=1)
        second_work_end = date + timedelta(hours=10, minutes=1)
        third_work_end = date + timedelta(hours=18, minutes=1)
        self.schedule_message(finish_work_text, first_work_end)
        self.schedule_message(finish_work_text, second_work_end)
        self.schedule_message(finish_work_text, third_work_end)
