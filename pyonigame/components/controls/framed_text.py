from typing import Callable

from pyonigame.components.controls._framed_base import FramedBase
from pyonigame.components.base import EventBase
from pyonigame.events import Event
from pyonigame.components.core import Text, Rect


class Style:
    def __init__(self, font, size, bg_color, text_color, border_color=(0, 0, 0), padding=20, border_radius=10, border_width=5, bold=False):
        self.font = font
        self.size = size
        self.background_color = bg_color
        self.text_color = text_color
        self.border_color = border_color
        self.padding = padding
        self.border_width = border_width
        self.border_radius = border_radius
        self.bold = bold

    @staticmethod
    def test_title(font, size, **kwargs):
        return Style(font, size, (205, 133, 63), (128, 0, 32), (139, 69, 19), **kwargs)

    @staticmethod
    def title(font, size, **kwargs):
        return Style(font, size, (205, 133, 63), (255, 245, 238), (139, 69, 19), **kwargs)


class FramedText(FramedBase):

    Layer = Text.Layer

    def __init__(self, x, y, width, height, text: str, style: Style, layer=Text.Layer.CONTROL, event_subscription: Event = Event.NONE):
        super().__init__(Text, style, x, y, width, height, text, layer, event_subscription)
        self.resize(width, height)

    def create(self, rect_type, text_type, *args) -> (Rect, Text):
        x, y, width, height, text, layer, event_subscription = args
        rect = rect_type(self, x, y, width, height, self.style.background_color, border_color=self.style.border_color,
                         border_radius=self.style.border_radius, border_width=self.style.border_width, layer=layer,
                         event_subscription=event_subscription)

        text = text_type(self, text, self.style.font, self.style.size, self.style.text_color, 0, 0,
                         layer=layer, event_subscription=Event.NONE, bold=self.style.bold)
        return rect, text

    def set(self, x, y):
        self.rect.set(x, y)
        self.align_text_coordinates()

    def align_text_coordinates(self):
        self.text.x = self.x + (self.width - self.text.width) // 2
        self.text.y = self.y + (self.height - self.text.height) // 2

    def resize(self, width, height):
        self.rect.resize(width, height)
        self.text.resize(width - self.style.padding, height - self.style.padding)

    def resolve_text_shape(self, child: EventBase, get_font_shape: Callable[[str, str, int], tuple[int, int]]):
        self.align_text_coordinates()
