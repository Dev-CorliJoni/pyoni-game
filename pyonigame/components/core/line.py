from typing import Union
from pyonigame.components.base import EventBase, ColorBase
from pyonigame.events import Event


class Line(EventBase, ColorBase):
    def __init__(self, size, color: Union[tuple[float, float, float], str], pos1: tuple[int, int], pos2: tuple[int, int], layer=EventBase.Layer.GAME_ELEMENT, event_subscription: Event = Event.NONE):
        super().__init__("line", layer, event_subscription)
        ColorBase.__init__(self, color=color)

        self.pos1 = pos1
        self.pos2 = pos2
        self.size = size

    def set1(self, x, y):
        self.pos1 = (x, y)

    def set2(self, x, y):
        self.pos2 = (x, y)
