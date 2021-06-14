from datetime import datetime

from telethon import utils
from telethon.tl import functions

from src.base.settings import Settings
from src.base.tg_client import get_client, APIClient


async def get_chat_id_from_invite(invite_hash):
    c = get_client()

    result = await c(functions.messages.CheckChatInviteRequest(
        hash=invite_hash
    ))

    return result.chat.id


async def resolve_chat_id(s):
    chat_id = s.chat_id

    if chat_id is None and s.invite_hash is not None:
        chat_id = await get_chat_id_from_invite(s.invite_hash)
    elif s.invite_hash is None:
        raise Exception("Either 'chat_id' or 'invite_hash' should be specified")

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
        self.chat_id = chat_id
        self.client = get_client()

    def send_message(self, message: str, **kwargs):
        return self.client.send_message(recipient=self.chat_id,
                                        message=message, **kwargs)

    def schedule_message(self, message: str, schedule: datetime, **kwargs):
        return self.client.schedule_message(recipient=self.chat_id,
                                            schedule=schedule,
                                            message=message, **kwargs)

    def messages_of(self, *args, **kwargs):
        return self.client.messages_of(*args, **kwargs)
