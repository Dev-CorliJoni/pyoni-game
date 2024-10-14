from typing import Union

from pyonigame.elements.base import ClickableBase, ColorBase


class Rect(ClickableBase, ColorBase):

    def __init__(self, x, y, width, height, color: Union[tuple[float, float, float], str], border_color: Union[tuple[float, float, float], str] = "transparent", layer=ClickableBase.Layer.GAME_ELEMENT, border_radius=0, border_width=5, click_event=None):
        super().__init__("rect", layer, x, y, width, height, click_event)
        ColorBase.__init__(self, color=color)

        self.border_color = border_color
        self.border_width = border_width
        self.border_radius = border_radius
