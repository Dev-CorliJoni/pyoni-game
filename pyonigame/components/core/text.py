from typing import Callable
from pyonigame.components.base import EventBase, ColorBase, ShapeBase, CoordinateBase
from pyonigame.events import Event


class Text(EventBase, CoordinateBase, ShapeBase, ColorBase):
    def __init__(self, text, font, size, color: tuple[float, float, float], x, y, layer=EventBase.Layer.CONTROL, event_subscription: Event = Event.NONE, bold=False):
        super().__init__("text", layer, event_subscription)
        CoordinateBase.__init__(self, x, y)
        ShapeBase.__init__(self, 0, 0)
        ColorBase.__init__(self, color=color)

        self.text = text
        self.font = font
        self._default_size = size
        self._resize_target = None
        self.size = size
        self.bold = bold
        self.request_text_shape_resolver()

    def calculate_size(self, get_font_shape: Callable[[str, str, int], tuple[int, int]]):
        self.width, self.height = get_font_shape(self.text, self.font.value, self.size)

    def resolve_text_shape(self, get_font_shape: Callable[[str, str, int], tuple[int, int]]):
        if self._resize_target is None:
            self.calculate_size(get_font_shape)
        else:
            width, height = self._resize_target
            self.size = self._default_size
            self.calculate_size(get_font_shape)

            while self.width < width and self.height < height:
                self.size += 1
                self.calculate_size(get_font_shape)

            while self.size > 1:
                self.size -= 1
                self.calculate_size(get_font_shape)

                if self.width <= width and self.height <= height:
                    break

    def resize(self, width, height):
        self._resize_target = width, height
        self.request_text_shape_resolver()

    def update(self, passed_time):
        data = super().update(passed_time)
        data.font = self.font.value
        return data

