from datetime import datetime

from telethon import utils

from base.settings import Settings
from base.tg_client import get_client, APIClient


def resolve_chat_id(s):
    chat_id = s.chat_id

    if chat_id is None:
        raise Exception("No 'chat_id' was specified")

    if chat_id < 0:
        real_id, peer_type = utils.resolve_id(chat_id)
        chat_id = real_id

    return chat_id


def from_settings(settings: Settings):
    chat_id = resolve_chat_id(settings)
    return Chat(chat_id)


class Chat:
    chat_id: int
    client: APIClient

    def __init__(self, chat_id):
        self.chat_id = self.resolve_chat_id(chat_id)
        self.client = get_client()

    @staticmethod
    def resolve_chat_id(chat_id):
        if chat_id < 0:
            return utils.resolve_id(chat_id)
        return chat_id

    def send_message(self, message: str, **kwargs):
        return self.client.send_message(recipient=self.chat_id,
                                        message=message, **kwargs)

    def schedule_message(self, message: str, schedule: datetime, **kwargs):
        return self.client.schedule_message(recipient=self.chat_id,
                                            schedule=schedule, silent=True,
                                            message=message, **kwargs)

    def messages_of(self, *args, **kwargs):
        return self.client.messages_of(*args, **kwargs)
