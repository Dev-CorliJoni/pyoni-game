from __future__ import annotations


from pyonigame.models import DictObject
from pyonigame.models.settings.helper import from_dict_obj


class DisplayDimension(DictObject):
    def __init__(self, width: int, height: int):
        super().__init__(width=width, height=height)

    def set_dimension(self, width: int, height: int):
        self.width = width
        self.height = height

    @property
    def width(self) -> int:
        return super().width

    @width.setter
    def width(self, width: int) -> None:
        super().width = width

    @property
    def height(self) -> int:
        return super().height

    @height.setter
    def height(self, height: int) -> None:
        super().height = height

    @staticmethod
    def from_dict_object(dict_object: DictObject) -> DisplayDimension:
        width = from_dict_obj(dict_object, "width", 800)
        height = from_dict_obj(dict_object, "height", 600)
        return DisplayDimension(width, height)
