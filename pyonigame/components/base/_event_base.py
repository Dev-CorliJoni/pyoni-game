from pyonigame.elements.base import Base
from pyonigame.events import Request, Event
from pyonigame.events.event_controller import EventController


class EventBase(Base):

    def __init__(self, type_, layer, event_subscription: Event):
        super().__init__(type_, layer)
        self.focus_order_number = None
        self.set_event_subscriptions(event_subscription)

    def set_event_subscriptions(self, event_subscriptions: Event):
        EventController.set_event_subscriptions(self, event_subscriptions)

    def request(self, request: Request):
        EventController.request(request, self)

    def theme_changed(self, theme):
        pass

    def language_changed(self, language):
        pass

    def screen_size_changed(self, width, height):
        pass

    def left_click(self, mouse_x, mouse_y):
        pass

    def middle_click(self, mouse_x, mouse_y):
        pass

    def right_click(self, mouse_x, mouse_y):
        pass

    def hover(self, mouse_x, mouse_y):
        pass

    def focus(self, mouse_x, mouse_y):
        pass

    def lost_focus(self):
        pass

    def drag_start(self, mouse_x, mouse_y):
        pass

    def dragging(self, mouse_x, mouse_y):
        pass

    def drop(self, mouse_x, mouse_y):
        pass

    def scroll_up(self):
        pass

    def scroll_down(self):
        pass

    def key_press(self, unicode, value, mapped_value):
        pass

    def key_release(self, unicode, value, mapped_value):
        pass
