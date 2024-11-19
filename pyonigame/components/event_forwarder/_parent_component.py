from typing import Callable

from pyonigame.components.base import EventBase
from pyonigame.events import RequestProvider
from pyonigame.models.settings import Theme, Language


class ParentComponent(RequestProvider):

    def __init__(self):
        pass

    def resolve_text_shape(self, child: EventBase, get_font_shape: Callable[[str, str, int], tuple[int, int]]):
        pass

    def theme_changed(self, child: EventBase, theme: Theme):
        pass

    def language_changed(self, child: EventBase, language: Language):
        pass

    def screen_size_changed(self, child: EventBase, width: int, height: int):
        pass

    def left_click(self, child: EventBase, mouse_x: int, mouse_y: int):
        pass

    def middle_click(self, child: EventBase, mouse_x: int, mouse_y: int):
        pass

    def right_click(self, child: EventBase, mouse_x: int, mouse_y: int):
        pass

    def hover(self, child: EventBase, mouse_x: int, mouse_y: int):
        pass

    def focus(self, child: EventBase, mouse_x: int, mouse_y: int):
        pass

    def lost_focus(self, child: EventBase):
        pass

    def drag_start(self, child: EventBase, mouse_x: int, mouse_y: int):
        pass

    def dragging(self, child: EventBase, mouse_x: int, mouse_y: int):
        pass

    def drop(self, child: EventBase, mouse_x: int, mouse_y: int):
        pass

    def scroll_up(self, child: EventBase):
        pass

    def scroll_down(self, child: EventBase):
        pass

    def key_press(self, child: EventBase, unicode: str, value: str, mapped_value: str):
        pass

    def key_release(self, child: EventBase, unicode: str, value: str, mapped_value: str):
        pass


