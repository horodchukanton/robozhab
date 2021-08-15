import logging
from datetime import datetime, timedelta
from game import from_settings
from base.settings import get_settings

logging.basicConfig(
    format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
    level=logging.INFO)

scheduled_days = 5


def main():
    settings = get_settings()
    game = from_settings(settings)

    for i in range(scheduled_days):
        date = datetime.now(tz=settings.tz) + timedelta(days=i)
        game.schedule_day(date)

main()

# # MAIN
# with TelegramClient('anon', api_id, api_hash) as client:
#     client.loop.run_until_complete(main(client))
