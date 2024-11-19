from typing import Union
from pyonigame.components.base import CoordinateBase, ColorBase, EventBase
from pyonigame.events import Event


class Circle(EventBase, CoordinateBase, ColorBase):

    def __init__(self, x, y, radius, color: Union[tuple[float, float, float], str], layer=EventBase.Layer.GAME_ELEMENT, event_subscription: Event = Event.NONE):
        super().__init__("circle", layer, event_subscription)
        CoordinateBase.__init__(self, x=x, y=y)
        ColorBase.__init__(self, color=color)

        self.radius = radius
