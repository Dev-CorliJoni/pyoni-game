from typing import Callable

from pyonigame.components.base import EventBase
from pyonigame.events import RequestProvider
from pyonigame.models.settings import Theme, Language


class ParentComponent(RequestProvider):
    """
    A base class for managing and handling events from child components.

    `ParentComponent` is designed to be inherited by classes that need to coordinate and respond to events (e.g., clicks, focus changes, theme updates) from multiple child components.
    It provides a unified interface to handle these events, receiving information about the child that triggered the event.

    To use, inherit from `ParentComponent` and implement any event methods needed (e.g., `left_click`, `theme_changed`). The parent instance will automatically receive events forwarded from children decorated with `@child_component`.

    Example:
        # In this example, the parent is notified when one of two rectangles is clicked.

        from pyonigame.events import Event

         class MyParentComponent(ParentComponent):
            def __init__(self):
                child_type = create_child_component_type(Rect)
                black = (0, 0, 0)
                self.children = [
                    child_type(self, 0, 0, 20, 20, black, event_subscription = Event.MOUSE),
                    child_type(self, 20, 0, 20, 20, black, event_subscription = Event.MOUSE),
                ]

            def update(passed_time):
                return [child.update(passed_time) for child in self.children]

            def left_click(self, child, mouse_x, mouse_y):
                print(f"{child.id} clicked at ({mouse_x}, {mouse_y})")
    """
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
