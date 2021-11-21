import logging
import injector

from robozhab.base.tg_client import APIClient
from robozhab.base.settings import get_settings, Settings
from robozhab.game import Game

logging.basicConfig(
    format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
    level=logging.INFO)


class Main(injector.Module):
    def __init__(self, config_path: str) -> None:
        self._config_path = config_path

    @injector.provider
    def _settings(self) -> Settings:
        return get_settings(self._config_path)

    @injector.provider
    def _tg_client(self, settings: Settings) -> APIClient:
        return APIClient(settings)

    @injector.provider
    def _game(self, settings: Settings, client: APIClient) -> Game:
        return Game(client, settings)
