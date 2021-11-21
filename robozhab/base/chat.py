from datetime import datetime

from telethon import utils
from robozhab.base.tg_client import APIClient


class Chat:
    chat_id: int
    client: APIClient

    def __init__(self, client: APIClient, chat_id: int):
        self.chat_id = self.resolve_chat_id(chat_id)
        self.client = client

    @staticmethod
    def resolve_chat_id(chat_id):
        if chat_id is None:
            raise Exception("No 'chat_id' was specified")

        if chat_id < 0:
            chat_id, peer_type = utils.resolve_id(chat_id)
            assert peer_type

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
