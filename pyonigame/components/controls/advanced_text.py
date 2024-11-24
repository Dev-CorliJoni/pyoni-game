from typing import Callable

from pyonigame.components.base import EventBase
from pyonigame.events import Event
from pyonigame.components.core import AlignableText, Rect
from pyonigame.components.event_forwarder import create_child_component_type, ParentComponent


class Style:
    def __init__(self, font, size, bg_color, text_color, border_color=(0, 0, 0), padding=20, border_radius=10, border_width=5):
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


class AdvancedText(ParentComponent):

    Layer = AlignableText.Layer

    def __init__(self, text: str, style, x_percent, y_percent, height_percent, layer=AlignableText.Layer.CONTROL, event_subscription: Event = Event.NONE):
        self.style = style
        self._height_percent = height_percent

        text_type = create_child_component_type(AlignableText)
        self.text = text_type(self, text, style.font, style.size, style.text_color, x_percent, y_percent, layer, event_subscription)
        self.rect = Rect(0, 0, 0, 0, style.background_color, border_color=style.border_color, layer=layer, border_radius=style.border_radius, border_width=style.border_width)

    def update(self, inputs, **kwargs):
        # Todo Remove self.set_text_form(supress_coordinate_reset=True)
        text_update = self.text.update(inputs)  # Todo Remove, post_change_func=self.set_coordinates, **kwargs)
        return [self.rect.update(inputs), text_update]

    def screen_size_changed(self, child: EventBase, width: int, height: int):
        self.text.resize_by_height(height * self._height_percent)

    def resolve_text_shape(self, child: EventBase, get_font_shape: Callable[[str, str, int], tuple[int, int]]):
        self.set_coordinates()

    def set_text_form(self, supress_coordinate_reset=False):
        # Todo is method still necessary ?
        self.text.resize_by_height(self.settings.view.dimension.height * self._height_percent)
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

    @property
    def any_state_changed(self):
        return self.text.state_changed or self.rect.state_changed

    @any_state_changed.setter
    def any_state_changed(self, value):
        self.text.state_changed = value
        self.rect.state_changed = value

    @property
    def x(self):
        return self.rect.x

    @property
    def y(self):
        return self.rect.y

    @property
    def width(self):
        return self.rect.width

    @property
    def height(self):
        return self.rect.height
