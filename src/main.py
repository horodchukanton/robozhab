import logging
from base.settings import get_settings
from game import Game

logging.basicConfig(
    format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
    level=logging.INFO)


def main():
    settings = get_settings()
    game = Game.from_settings(settings)
    game.schedule()


main()
