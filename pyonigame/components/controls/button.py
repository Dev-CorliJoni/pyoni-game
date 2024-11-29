from functools import partial
from typing import Callable

from pyonigame.components.base import EventBase
from pyonigame.components.controls import FramedText, FramedTextStyle
from pyonigame.events import Event


class Style(FramedTextStyle):
    def __init__(self, font, size, bg_color, active_bg_color, text_color, border_color=(0, 0, 0), border_radius=10, border_width=5, padding=5):
        super().__init__(font, size, bg_color, text_color, border_color, padding, border_radius, border_width)
        self.active_background_color = active_bg_color

    @staticmethod
    def for_slider(font, size, **kwargs):
        return Style(font, size, (255, 255, 255), (220, 220, 220), (0, 0, 0), border_width=0, **kwargs)

    @staticmethod
    def on_gras(font, size, **kwargs):
        return Style(font, size, (139, 69, 19), (128, 0, 32), (200, 200, 200), (205, 133, 63), **kwargs)


class Button(FramedText):

    def __init__(self, x, y, width, height, text, style, click_event: Callable[[int, int], None], layer=FramedText.Layer.CONTROL, event_subscription: Event = Event.NONE):  # Todo Remove , _x_percent=0, _y_percent=0, _height_percent=0):
        super().__init__(x, y, width, height, text, style, layer=layer, event_subscription=Event.MOUSE | Event.FOCUS | Event.KEY | event_subscription)

        self.active = False
        self.hovering = False
        self.click_event = click_event

    def update(self, passed_time: float):
        self.refresh_color()
        return super().update(passed_time)

    def left_click(self, child: EventBase, mouse_x: int, mouse_y: int):
        self.click_event(mouse_x, mouse_y)

    def hover(self, child: EventBase, mouse_x: int, mouse_y: int):
        self.hovering = True

    # Todo Remove
    """
    def resize(self, width, height, adjust_over_text_height=False):
        if adjust_over_text_height:
            # Todo this way has to be updated
            self.text.resize_by_height(height - self.style.padding)
            self.rect.resize(self.text.width + self.style.padding, height)
        else:
            self.rect.resize(width, height)
            self.text.resize(width - self.style.padding, height - self.style.padding)"""

    def focus(self):
        self.rect.focus()

    def on_focus(self, child: EventBase, mouse_x: int, mouse_y: int):
        print("Gained focus")
        self.active = True

    def lost_focus(self, child: EventBase):
        print("Lost focus")
        self.active = False

    def key_press(self, child: EventBase, unicode: str, value: str, mapped_value: str):
        if value == "return" and self.active:
            self.click_event(-1, -1)

    @property
    def hover_color(self):
        return tuple(min(val + 10, 255) for val in self.style.active_background_color)

    def refresh_color(self):
        if self.hovering and self.rect.color != self.hover_color:
            self.rect.color = self.hover_color
            self.hovering = False
        elif self.active:
            self.rect.color = self.style.active_background_color
        elif self.rect.color != self.style.background_color:
            self.rect.color = self.style.background_color
