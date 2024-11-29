from abc import ABC, abstractmethod

from pyonigame.components.core import Text, Rect
from pyonigame.components.event_forwarder import ParentComponent, create_child_component_type


class FramedBase(ParentComponent, ABC):

    def __init__(self, text_type: type[Text], style, *args):
        self.style = style
        self.rect, self.text = self.create(create_child_component_type(Rect), create_child_component_type(text_type), *args)

    @abstractmethod
    def create(self, rect_type, text_type, *args) -> (Rect, Text):
        pass

    def update(self, passed_time: float):
        self.text.state_changed = self.text.state_changed or self.rect.state_changed
        return [self.rect.update(passed_time), self.text.update(passed_time)]

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
