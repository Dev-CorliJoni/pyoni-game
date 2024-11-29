from typing import Callable

from pyonigame.events import Event

from pyonigame.components.core import Text


class ResponsiveText(Text):
    def __init__(self, text, font, size, color: tuple[float, float, float], x_percent: float, y_percent: float, layer=Text.Layer.CONTROL, event_subscription: Event = Event.NONE):
        super().__init__(text, font, size, color, 0, 0, layer=layer, event_subscription=event_subscription | Event.SCREEN_SIZE_CHANGED)
        self._x_percent = float(x_percent)
        self._y_percent = float(y_percent)

    def set_relative_coordinates(self):
        self.set(*self.get_coordinates_by_percentage(self.settings.view.dimension, self._x_percent, self._y_percent, self.width, self.height))

    def screen_size_changed(self, width: int, height: int):
        self.set_relative_coordinates()

    def resolve_text_shape(self, get_font_shape: Callable[[str, str, int], tuple[int, int]]):
        super().resolve_text_shape(get_font_shape)
        self.set_relative_coordinates()

    def update(self, passed_time: float):  # Todo remove if it works without this > , supress_coordinate_reset=False, **kwargs):
        # Todo remove if it works in Button without this Functionality
        # if supress_coordinate_reset is False:
        #    self.set_relative_coordinates()
        update_obj = super().update(passed_time)  # Todo remove if it works without this -> , **kwargs)
        return update_obj

