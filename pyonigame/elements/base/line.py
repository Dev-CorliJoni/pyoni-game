from typing import Union
from pyonigame.elements.base import Base, ColorBase


class Line(Base, ColorBase):
    def __init__(self, size, color: Union[tuple[float, float, float], str], pos1: tuple[int, int], pos2: tuple[int, int], layer=Base.Layer.GAME_ELEMENT):
        super().__init__("line", layer)
        ColorBase.__init__(self, color=color)

        self.size = size

        self.pos1 = pos1
        self.pos2 = pos2

    def set1(self, x, y):
        self.pos1 = (x, y)

    def set2(self, x, y):
        self.pos2 = (x, y)
