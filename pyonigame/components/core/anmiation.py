from pyonigame.components.base import ImageBase
from pyonigame.events import Event


class Animation(ImageBase):

    def __init__(self, image_path, *animation_coordinates, x, y, interval, layer=ImageBase.Layer.GAME_ELEMENT, event_subscription: Event = Event.NONE, scale_factor=1, image_rotation=0, mirror_x=False, mirror_y=False):
        width, height = animation_coordinates[0][2] * scale_factor, animation_coordinates[0][3] * scale_factor
        super().__init__("animation", layer, image_path, x, y, width, height, scale_factor, image_rotation, mirror_x, mirror_y, event_subscription)

        self._interval = interval
        self._current_interval = interval

        self.animation_coordinates = animation_coordinates
        self.current_image = 0

    def update(self, inputs, **kwargs):
        passed_time = float(next(filter(lambda i: i.type == "passed_time", inputs)).value)

        self._current_interval -= passed_time
        if self._current_interval <= 0:
            self._current_interval = self._interval
            self.current_image = (self.current_image + 1) % len(self.animation_coordinates)

        return super().update(inputs, **kwargs)
