from datetime import datetime
from functools import lru_cache

from telethon.sync import TelegramClient
from telethon.tl import types

from base.settings import Settings, get_settings


@lru_cache(maxsize=1)
def get_client():
    return APIClient()


class APIClient:
    telethon: TelegramClient
    settings: Settings

    def __init__(self):
        self.telethon = self.login()
        self.settings = get_settings()

    def login(self):
        settings = get_settings()
        # Use your own values from my.telegram.org
        api_id = settings.api_id
        api_hash = settings.api_hash

        client = TelegramClient('anon', api_id, api_hash).start()

        client.connect()
        return client

    def send_message(self, recipient: id, message: str, **kwargs):
        """Sends message to the chat"""
        self.telethon.send_message(entity=types.PeerChannel(recipient),
                                   message=message, **kwargs)

    def schedule_message(self, recipient: id, message: str, schedule: datetime,
                         **kwargs):
        """Sends message to the chat at given time.
        If the time is in past, will skip sending and return false"""

        if datetime.now(tz=self.settings.tz) > schedule:
            return False

        return self.send_message(recipient=recipient,
                                 message=message,
                                 schedule=schedule,
                                 **kwargs)

    def messages_of(self, sender: str = 'me', **kwargs):
        if not kwargs['limit']:
            kwargs['limit'] = 300

        return self.telethon.iter_messages(entity=sender, from_user=sender,
                                           **kwargs)

    def __del__(self):
        self.telethon.disconnect()
