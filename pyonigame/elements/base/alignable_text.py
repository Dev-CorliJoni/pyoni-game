from pyonigame.elements.base import Text


class AlignableText(Text):
    def __init__(self, text, font, size, color: tuple[float, float, float], x_percent, y_percent, get_font_dimension, get_dimension, layer=Text.Layer.CONTROL, click_event=None):
        self._get_dimension = get_dimension

        self._x_percent = float(x_percent)
        self._y_percent = float(y_percent)

        super().__init__(text, font, size, color, 0, 0, get_font_dimension, layer=layer, click_event=click_event)
        self.x, self.y = self.get_coordinates_by_percentage(self._get_dimension(), self._x_percent, self._y_percent, self.width, self.height)

    def set_calculate_relative_coordinates(self):
        self.set(*self.get_coordinates_by_percentage(self._get_dimension(), self._x_percent, self._y_percent, self.width, self.height))

    def update(self, inputs, supress_coordinate_reset=False, **kwargs):
        if supress_coordinate_reset is False:
            self.set_calculate_relative_coordinates()
        update_obj = super().update(inputs, **kwargs)
        return update_obj

