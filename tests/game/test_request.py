from mockito import mock, when, ANY
from pytest import fixture
from telethon.tl.types import Message

from base.chat import Chat
from base.settings import Settings
from game.request import ZhabaInfoRequester


class TestZhabaInfoRequest:

    @fixture
    def chat(self):
        chat = mock(Chat)
        when(chat).send_message("Жаба инфо").thenReturn(None)
        when(chat).messages_of(sender=ANY).thenReturn([Message(
            date=None,
            peer_id=None,
            id=None,
            message="""🍭:Жабу можно покормить
(Можно откормить)
🏃‍♂️:Жабу можно отправить на работу
⚔️:Не участвует в дуэли
☠️:Можно отправиться в подземелье
💃:Можно пойти на тусу
💘:Сізіф и Арсен Борисович"""
        )
        ])

    @fixture
    def settings(self):
        return Settings()

    def test_sanity(self, settings, chat):
        requester = ZhabaInfoRequester(settings, chat)

        info = requester.request()
