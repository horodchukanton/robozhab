from unittest import mock

from _pytest.fixtures import fixture

from robozhab.base.chat import Chat, from_settings
from robozhab.base.settings import Settings


class TestChat:

    @fixture
    def client(self):
        return mock.Mock(Chat, autospec=True)

    @fixture()
    def settings(self):
        return Settings()

    def test_sanity(self, settings):
        chat = from_settings(settings)
        assert chat
