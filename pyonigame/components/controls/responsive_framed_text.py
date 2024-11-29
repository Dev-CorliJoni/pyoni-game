from typing import Callable

from components.core import Text
from pyonigame.components.controls._framed_base import FramedBase
from pyonigame.components.base import EventBase
from pyonigame.events import Event
from pyonigame.components.core import ResponsiveText, Rect
from pyonigame.components.event_forwarder import create_child_component_type, ParentComponent


class Style:
    def __init__(self, font, size, bg_color, text_color, border_color=(0, 0, 0), padding=20, border_radius=10,
                 border_width=5):
        self.font = font
        self.size = size
        self.background_color = bg_color
        self.text_color = text_color
        self.border_color = border_color
        self.padding = padding
        self.border_width = border_width
        self.border_radius = border_radius

    @staticmethod
    def test_title(font, size, **kwargs):
        return Style(font, size, (205, 133, 63), (128, 0, 32), (139, 69, 19), **kwargs)

    @staticmethod
    def title(font, size, **kwargs):
        return Style(font, size, (205, 133, 63), (255, 245, 238), (139, 69, 19), **kwargs)


class ResponsiveFramedText(FramedBase):

    Layer = ResponsiveText.Layer

    def __init__(self, text: str, style, x_relative_position, y_relative_position, relative_height, layer=ResponsiveText.Layer.CONTROL, event_subscription: Event = Event.NONE):
        super().__init__(ResponsiveText, style, text, x_relative_position, y_relative_position, layer, event_subscription)
        self._relative_height = relative_height

    def create(self, rect_type, text_type, *args) -> (Rect, Text):
        text, x_relative_position, y_relative_position, layer, event_subscription = args
        rect = rect_type(self, 0, 0, 0, 0, self.style.background_color, border_color=self.style.border_color,
                         border_radius=self.style.border_radius, border_width=self.style.border_width, layer=layer,
                         event_subscription=event_subscription)
        text = text_type(self, text, self.style.font, self.style.size, self.style.text_color,
                         x_relative_position, y_relative_position, layer=layer, event_subscription=event_subscription)
        return rect, text

    @property
    def relative_height(self):
        return self._relative_height

    @relative_height.setter
    def relative_height(self, relative_height):
        self._relative_height = relative_height
        self.recalculate_shape()

    # Todo Remove
    """    def update(self, passed_time: float, **kwargs):
        # Todo Remove self.set_text_form(supress_coordinate_reset=True)
        text_update = self.text.update(passed_time)  # Todo Remove, post_change_func=self.set_coordinates, **kwargs)
        return [self.rect.update(passed_time), text_update]"""

    def recalculate_shape(self):
        self.text.resize_by_height(self.settings.view.dimension.height * self._relative_height)

    def screen_size_changed(self, child: EventBase, width: int, height: int):
        if self.text is child:
            self.recalculate_shape()

    def resolve_text_shape(self, child: EventBase, get_font_shape: Callable[[str, str, int], tuple[int, int]]):
        self.set_coordinates()

    def set_text_form(self, supress_coordinate_reset=False):
        # Todo is method still necessary ?
        self.text.resize_by_height(self.settings.view.dimension.height * self._relative_height)
        if supress_coordinate_reset is False:
            self.text.set_relative_coordinates()

    def set_coordinates(self):
        dimension = self.settings.view.dimension
        txt_width, txt_height = self.text.width, self.text.height

        y_padding = self.style.padding / 8

        self.rect.set(self.text.x - self.style.padding, self.text.y - y_padding)
        self.rect.resize(txt_width + self.style.padding * 2, txt_height + y_padding * 2)

        if dimension.width < self.rect.x + self.rect.width + self.style.padding:
            self.rect.x = dimension.width - self.rect.width - self.style.padding

        if dimension.height < self.rect.y + self.rect.height + y_padding:
            self.rect.y = dimension.height - self.rect.height - y_padding

        if 0 > self.rect.x - self.style.padding:
            self.rect.x = self.style.padding

        if 0 > self.rect.y - y_padding:
            self.rect.y = y_padding

        self.text.set(self.x + self.style.padding, self.y + y_padding)
