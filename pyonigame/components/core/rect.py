from typing import Union

from pyonigame.components.base import CoordinateBase, ShapeBase, ColorBase, EventBase
from pyonigame.events import Event


class Rect(EventBase, CoordinateBase, ShapeBase, ColorBase):

    def __init__(self, x, y, width, height, color: Union[tuple[float, float, float], str], border_color: Union[tuple[float, float, float], str] = "transparent", layer=EventBase.Layer.GAME_ELEMENT, event_subscription: Event = Event.NONE, border_radius=0, border_width=5):
        super().__init__("rect", layer, event_subscription)
        CoordinateBase.__init__(self, x, y)
        ShapeBase.__init__(self, width, height)
        ColorBase.__init__(self, color=color)

        self.border_color = border_color
        self.border_width = border_width
        self.border_radius = border_radius

