from datetime import datetime

from telethon.sync import TelegramClient
from telethon.tl import types

from robozhab.base.settings import Settings


class APIClient:
    telethon: TelegramClient
    settings: Settings

    def __init__(self, settings: Settings):
        self.telethon = self.login(settings)
        self.tz = settings.tz

    @staticmethod
    def login(settings: Settings):
        api_id = settings.api_id
        api_hash = settings.api_hash

        client = TelegramClient('anon', api_id, api_hash).start()

        client.connect()
        return client

    def send_message(self, recipient: id, message: str, **kwargs):
        """Sends message to the chat"""
        return self.telethon.send_message(entity=types.PeerChannel(recipient),
                                          message=message, **kwargs)

    def schedule_message(self, recipient: id, message: str, schedule: datetime,
                         **kwargs):
        """Sends message to the chat at given time.
        If the time is in past, will skip sending and return false"""

        if datetime.now(tz=self.tz) > schedule:
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
        if not self.telethon:
            return
        self.telethon.disconnect()
