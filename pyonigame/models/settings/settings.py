from __future__ import annotations

from typing import cast

from pyonigame.helper import IODictObject
from pyonigame.models import DictObject
from pyonigame.models.settings import GameSettings, ViewSettings
from pyonigame.models.settings.helper import from_dict_obj


class Settings(DictObject):
    def __init__(self, view: ViewSettings, game: GameSettings):
        super().__init__(view=view, game=game)

    @property
    def view(self) -> ViewSettings:
        return super().view

    @view.setter
    def view(self, view: ViewSettings) -> None:
        super().view = view

    @property
    def game(self) -> GameSettings:
        return cast(GameSettings, super().game)

    @game.setter
    def game(self, game: GameSettings) -> None:
        super().game = game

    @staticmethod
    def default_settings() -> Settings:
        return Settings.from_dict_object(DictObject())

    @staticmethod
    def from_dict_object(dict_object: DictObject) -> Settings:
        view = ViewSettings.from_dict_object(from_dict_obj(dict_object, "view", DictObject()))
        game = GameSettings.from_dict_object(from_dict_obj(dict_object, "game", DictObject()))
        return Settings(view, game)

    @staticmethod
    def load(path: str) -> Settings:
        dict_object = IODictObject(path).load()
        return Settings.from_dict_object(dict_object)

    def save(self, path: str) -> None:
        IODictObject(path).write(self)
