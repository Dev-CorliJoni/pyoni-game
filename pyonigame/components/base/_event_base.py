from typing import Callable

from pyonigame.models.settings import Theme, Language
from pyonigame.components.base import Base
from pyonigame.events import RequestProvider, Event, ApplicationManager, Request


class EventBase(Base, RequestProvider):

    def __init__(self, type_, layer, event_subscription: Event):
        super().__init__(type_, layer)
        RequestProvider.__init__(self)

        self.focus_order_number = None
        self.set_event_subscriptions(event_subscription)

    def set_event_subscriptions(self, event_subscriptions: Event):
        ApplicationManager.set_event_subscriptions(self, event_subscriptions)

    def request_text_shape_resolver(self):
        ApplicationManager.request(Request.text_shape_resolver(), self)

    def resolve_text_shape(self, get_font_shape: Callable[[str, str, int], tuple[int, int]]):
        pass

    def theme_changed(self, theme: Theme):
        pass

    def language_changed(self, language: Language):
        pass

    def screen_size_changed(self, width: int, height: int):
        pass

    def left_click(self, mouse_x: int, mouse_y: int):
        pass

    def middle_click(self, mouse_x: int, mouse_y: int):
        pass

    def right_click(self, mouse_x: int, mouse_y: int):
        pass

    def hover(self, mouse_x: int, mouse_y: int):
        pass

    def focus(self, mouse_x: int, mouse_y: int):
        pass

    def lost_focus(self):
        pass

    def drag_start(self, mouse_x: int, mouse_y: int):
        pass

    def dragging(self, mouse_x: int, mouse_y: int):
        pass

    def drop(self, mouse_x: int, mouse_y: int):
        pass

    def scroll_up(self):
        pass

    def scroll_down(self):
        pass

    def key_press(self, unicode: str, value: str, mapped_value: str):
        pass

    def key_release(self, unicode: str, value: str, mapped_value: str):
        pass
