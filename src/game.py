from datetime import timedelta, datetime

from base.chat import Chat, resolve_chat_id


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

        # Feed time ( Every 6 hours )
        feed_step = 6
        feed_text = "Покормить жабу"
        for i in range(0, 24, feed_step):
            feed_time = date + timedelta(hours=i, minutes=0)
            self.schedule_message(feed_text, feed_time)

        # Work time ( Every 8 hours )
        work_step = 8
        work_text = "Работа крупье"
        finish_work_text = "Завершить работу"
        for i in range(0, 24, work_step):
            work_time = date + timedelta(hours=i, minutes=0)
            finish_time = work_time + timedelta(hours=2, minutes=1)
            self.schedule_message(work_text, work_time)
            self.schedule_message(finish_work_text, finish_time)
