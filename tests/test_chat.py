from unittest import mock

from _pytest.fixtures import fixture

from robozhab.base.chat import Chat
from robozhab.base.settings import Settings


class TestChat:

    @fixture
    def client(self):
        return mock.Mock(Chat, autospec=True)

    @fixture()
    def settings(self):
        return Settings()

    def test_sanity(self, client, settings):
        chat = Chat(client, settings.chat_id)
        assert chat
