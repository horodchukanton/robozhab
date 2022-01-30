import abc

from base.chat import Chat
from base.settings import Settings
from robozhab.game.info import ZhabaInfo


class ZhabaInfoRequester(abc.ABC):

    command = "Жаба инфо"

    def __init__(self, settings: Settings, chat: Chat):
        self.settings = settings
        self.chat = chat

    def request(self) -> ZhabaInfo:
        message = self.chat.send_message(self.command)
        # Get time of the message

        # Wait before checking for the response

        # Check if have response

        # Wait for the result after our message
        response = self.chat.messages_of()
