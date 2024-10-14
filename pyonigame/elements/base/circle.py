from typing import Union
from pyonigame.elements.base import Base, CoordinateBase, ColorBase


class Circle(Base, CoordinateBase, ColorBase):

    def __init__(self, x, y, radius, color: Union[tuple[float, float, float], str], layer=Base.Layer.GAME_ELEMENT):
        super().__init__("circle", layer)
        CoordinateBase.__init__(self, x=x, y=y)
        ColorBase.__init__(self, color=color)

        self.radius = radius
