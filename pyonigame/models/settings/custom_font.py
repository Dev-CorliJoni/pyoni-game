from __future__ import annotations

from pyonigame.models import DictObject
from pyonigame.models.components import Font
from pyonigame.models.settings.helper import from_dict_obj


class CustomFont(DictObject):

    def __init__(self, name: str, font_path: str):
        super().__init__(name=name, font_path=font_path)
        font_name = name.upper().replace("-", "_")
        if not hasattr(Font, font_name):
            Font.add(font_name, name)

    @property
    def name(self) -> str:
        return super().name

    @name.setter
    def name(self, name: str) -> None:
        super().name = name

    @property
    def font_path(self) -> str:
        return super().font_path

    @font_path.setter
    def font_path(self, font_path: str) -> None:
        super().font_path = font_path

    @staticmethod
    def from_dict_object(dict_object: DictObject) -> CustomFont:
        name = from_dict_obj(dict_object, "name", None)
        font_path = from_dict_obj(dict_object, "font_path", None)
        return CustomFont(name, font_path)
