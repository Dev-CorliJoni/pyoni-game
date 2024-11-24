from pyonigame.models.components.image_data import AnimationData
from pyonigame.components.base import ImageBase
from pyonigame.events import Event


class Animation(ImageBase):

    def __init__(self, x, y, animation_data: AnimationData, layer=ImageBase.Layer.GAME_ELEMENT, event_subscription: Event = Event.NONE, scale_factor=1):
        super().__init__("animation", layer, x, y, 0, 0, (0, 0, 0, 0), "", scale_factor, 0, False, False, event_subscription)

        self._animation_data = animation_data
        self._current_index = -1
        self._current_interval = 0

    @property
    def _current_image(self):
        return self._animation_data[self._current_index]

    def _next_sprite(self):
        self._current_index = (self._current_index + 1) % len(self._animation_data)
        img = self._current_image

        self._current_interval = img.interval
        self.path = img.image_path
        self.width, self.height = img.width * self.image_scale, img.height * self.image_scale
        self.sprite_coordinates = img.locator_tuple()
        self.image_rotation = img.image_rotation
        self.image_mirrored_x, self.image_mirrored_y = img.mirror_x, img.mirror_y

    def update(self, passed_time: float):
        self._current_interval -= passed_time
        if self._current_interval <= 0:
            self._next_sprite()

        return super().update(passed_time)
