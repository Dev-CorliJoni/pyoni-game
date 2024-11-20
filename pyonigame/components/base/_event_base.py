from typing import Callable

from pyonigame.models.settings import Theme, Language
from pyonigame.components.base import Base
from pyonigame.events import RequestProvider, Event, ApplicationManager, Request


class EventBase(Base, RequestProvider):
    """
    Base class for handling event-driven UI elements.
    Derived classes can set event_subscription, override the necessary event handlers, and have them invoked when an event occurs.
    """

    def __init__(self, type_: str, layer: Base.Layer, event_subscription: Event):
        """
        :param type_: The type of the game element.
        :param layer: Specifies the hierarchical layer the element belongs to.
               Layers are arranged from back to front as follows: BACKGROUND -> GAME_ELEMENT -> CONTROL.
        :param event_subscription: Defines the events that the object will subscribe to
        """
        super().__init__(type_, layer)
        RequestProvider.__init__(self)

        self.focus_order_number = None
        self.set_event_subscriptions(event_subscription)

    def set_event_subscriptions(self, event_subscription: Event):
        """
        Sets the event subscriptions for the UI element.

        The following events are supported:
            - `Event.THEME_CHANGED`: Triggers the `theme_changed` method.
            - `Event.LANGUAGE_CHANGED`: Triggers the `language_changed` method.
            - `Event.SCREEN_SIZE_CHANGED`: Triggers the `screen_size_changed` method.
            - `Event.KEY`: Triggers the `key_press` and `key_release` methods.
            - `Event.MOUSE`: Triggers the `left_click`, `middle_click`, `right_click`,
                             `hover`, `scroll_up`, and `scroll_down` methods.
            - `Event.FOCUS`: Triggers the `focus` and `lost_focus` methods.
            - `Event.DRAG_AND_DROP`: Triggers the `drag_start`, `dragging`, and `drop` methods.
            - `Event.COLLISION`: Not yet implemented.

        :param event_subscription: Defines the events that the object will subscribe to
        """
        ApplicationManager.set_event_subscription(self, event_subscription)

    def request_text_shape_resolver(self):
        """
        This method can be called by derived classes to calculate the width and height of a text on the UI.
        Before the next game loop, the 'resolve_text_shape' method is invoked with a function to compute the text’s dimensions.
        """
        ApplicationManager.request(Request.text_shape_resolver(), self)

    def resolve_text_shape(self, get_font_shape: Callable[[str, str, int], tuple[int, int]]):
        """
        Invoked when `request_text_shape_resolver` was invoked before. This method should be overridden by derived classes.

        :param get_font_shape: A callable that calculates the width and height of the text given the text, font name, and size.
        """
        pass

    def theme_changed(self, theme: Theme):
        """
        Invoked when the application's theme changes.

        :param theme: The updated theme.
        """
        pass

    def language_changed(self, language: Language):
        """
        Invoked when the application's language changes.

        :param language: The updated language.
        """
        pass

    def screen_size_changed(self, width: int, height: int):
        """
        Invoked when the screen size changes.

        :param width: The new screen width.
        :param height: The new screen height.
        """
        pass

    def left_click(self, mouse_x: int, mouse_y: int):
        """
        Invoked when the object is clicked with the left mouse button.

        :param mouse_x: The x-coordinate of the mouse cursor.
        :param mouse_y: The y-coordinate of the mouse cursor.
        """
        pass

    def middle_click(self, mouse_x: int, mouse_y: int):
        """
        Invoked when the object is clicked with the middle mouse button.

        :param mouse_x: The x-coordinate of the mouse cursor.
        :param mouse_y: The y-coordinate of the mouse cursor.
        """
        pass

    def right_click(self, mouse_x: int, mouse_y: int):
        """
        Invoked when the object is clicked with the right mouse button.

        :param mouse_x: The x-coordinate of the mouse cursor.
        :param mouse_y: The y-coordinate of the mouse cursor.
        """
        pass

    def hover(self, mouse_x: int, mouse_y: int):
        """
        Invoked when the mouse is hovering over the object.

        :param mouse_x: The x-coordinate of the mouse cursor.
        :param mouse_y: The y-coordinate of the mouse cursor.
        """
        pass

    def focus(self, mouse_x: int, mouse_y: int):
        """
        Invoked when object is focused.

        :param mouse_x: The x-coordinate of the mouse cursor.
        :param mouse_y: The y-coordinate of the mouse cursor.
        """
        pass

    def lost_focus(self):
        """
        Invoked when the object has lost its focus.
        """
        pass

    def drag_start(self, mouse_x: int, mouse_y: int):
        """
        Invoked when the mouse is starting to drag the object.

        :param mouse_x: The x-coordinate of the mouse cursor.
        :param mouse_y: The y-coordinate of the mouse cursor.
        """
        pass

    def dragging(self, mouse_x: int, mouse_y: int):
        """
        Invoked while the mouse is dragging the object.

        :param mouse_x: The x-coordinate of the mouse cursor.
        :param mouse_y: The y-coordinate of the mouse cursor.
        """
        pass

    def drop(self, mouse_x: int, mouse_y: int):
        """
        Invoked when the mouse is dropping the object.

        :param mouse_x: The x-coordinate of the mouse cursor.
        :param mouse_y: The y-coordinate of the mouse cursor.
        """
        pass

    def scroll_up(self):
        """
        Invoked when the mouse wheel scrolls up while being over the object.
        """
        pass

    def scroll_down(self):
        """
        Invoked when the mouse wheel scrolls down while being over the object.
        """
        pass

    def key_press(self, unicode: str, value: str, mapped_value: str):
        """
        Invoked when a key is pressed.

        :param unicode: The Unicode representation of the key.
        :param value: The raw key value.
        :param mapped_value: The value mapped according to the Key Mapping in the 'Setting' Object.
        """
        pass

    def key_release(self, unicode: str, value: str, mapped_value: str):
        """
        Invoked when a key is released.

        :param unicode: The Unicode representation of the key.
        :param value: The raw key value.
        :param mapped_value: The value mapped according to the Key Mapping in the 'Setting' Object.
        """
        pass
