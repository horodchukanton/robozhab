import logging
from datetime import datetime, timedelta, timezone

from telethon import TelegramClient, utils
from telethon import functions

from settings import get_settings

logging.basicConfig(
    format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
    level=logging.INFO)

settings = get_settings()

# Use your own values from my.telegram.org
api_id = settings.api_id
api_hash = settings.api_hash

scheduled_days = 3
tz = timezone(timedelta(hours=int(settings.timezone)))


async def main(c):

    chat_id = settings.chat_id
    if chat_id is None and settings.invite_hash is not None:
        chat_id = await get_chat_id_from_invite(c, settings.invite_hash)
    elif settings.invite_hash is None:
        raise Exception("Either 'chat_id' or 'invite_hash' should be specified")

    if chat_id < 0:
        real_id, peer_type = utils.resolve_id(chat_id)
        chat_id = real_id

    for i in range(scheduled_days):
        date = datetime.now(tz=tz) + timedelta(days=i)
        await schedule_day(c, chat_id, date)


async def schedule_day(c: TelegramClient, chat_id:int, date: datetime):
    # Normalizing
    date = date.replace(hour=0, minute=0, second=0)

    # The main bot has a lag, so we should set up a one minute offset
    offset = get_next_offset()
    date = date + timedelta(minutes=offset)

    # Feed time ( Every 12 hours )
    feed_text = "Покормить жабу"
    first_feed = date + timedelta(hours=0, minutes=0)
    second_feed = date + timedelta(hours=12, minutes=0)
    await schedule_message(c, chat_id, feed_text, first_feed)
    await schedule_message(c, chat_id, feed_text, second_feed)

    # Work time ( Every 6 hours )
    work_text = "Работа крупье"
    first_work = date + timedelta(hours=0, minutes=0)
    second_work = date + timedelta(hours=8, minutes=0)
    third_work = date + timedelta(hours=16, minutes=0)
    await schedule_message(c, chat_id, work_text, first_work)
    await schedule_message(c, chat_id, work_text, second_work)
    await schedule_message(c, chat_id, work_text, third_work)

    # Finish work ( 2 hours after work )
    finish_work_text = "Завершить работу"
    first_work_end = date + timedelta(hours=2, minutes=1)
    second_work_end = date + timedelta(hours=10, minutes=1)
    third_work_end = date + timedelta(hours=18, minutes=1)
    await schedule_message(c, chat_id, finish_work_text, first_work_end)
    await schedule_message(c, chat_id, finish_work_text, second_work_end)
    await schedule_message(c, chat_id, finish_work_text, third_work_end)


async def schedule_message(c, chat_id, text, schedule_time):
    if datetime.now(tz=tz) > schedule_time:
        logging.debug("Skipping scheduling message for the past")
        return

    await c.send_message(entity=chat_id,
                         message=text, schedule=schedule_time)


async def send_message_to_chat(c, chat_id, text):
    await c.send_message(chat_id, text)


async def get_chat_id_from_invite(c, invite_hash):
    result = await c(functions.messages.CheckChatInviteRequest(
        hash=invite_hash
    ))
    print(result.stringify())

    return result.chat.id


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


# MAIN
with TelegramClient('anon', api_id, api_hash) as client:
    client.loop.run_until_complete(main(client))
