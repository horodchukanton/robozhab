import argparse
import logging
from robozhab.base.settings import get_settings
from robozhab.game import Game

logging.basicConfig(
    format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
    level=logging.INFO)


def main(settings_file: str = None):
    settings = get_settings(settings_file)
    game = Game.from_settings(settings)
    game.schedule()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Get configuration')
    parser.add_argument('--config',
                        type=str, nargs='?', help='path to config.env')

    args = parser.parse_args()
    main(args.config)
