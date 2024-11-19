import argparse
from pyonigame.models.settings import Settings


def main():
    parser = argparse.ArgumentParser(prog="pyoni-game")
    subparsers = parser.add_subparsers(dest="command")

    create_parser = subparsers.add_parser("create-settings", help="Create settings file")
    create_parser.add_argument("path", help="Path to settings file")

    args = parser.parse_args()

    if args.command == "create-settings":
        settings = Settings.default_settings()
        settings.save(args.path)
