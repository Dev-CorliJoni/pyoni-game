from PIL import Image

from pyonigame.models.components.sprite_data import SpriteData
from pyonigame.components.base import ImageBase
from pyonigame.events import Event


class Sprite(ImageBase):

    def __init__(self, x, y, sprite_data: SpriteData, layer=ImageBase.Layer.GAME_ELEMENT, event_subscription: Event = Event.NONE, scale_factor=1):
        self.sprite_coordinates = sprite_data.locator_tuple()
        if sprite_data.is_location_empty():
            width, height = Image.open(sprite_data.image_path).size
            width, height = width * scale_factor, height * scale_factor
            self.sprite_coordinates = (0, 0, width, height)
        elif sprite_data.is_location_valid():
            width, height = self.sprite_coordinates[2] * scale_factor, self.sprite_coordinates[3] * scale_factor
        else:
            raise ValueError("Sprite data x, y, width and height have to be set or all set to None!")

        super().__init__("sprite", layer, sprite_data.image_path, x, y, width, height, scale_factor, sprite_data.image_rotation, sprite_data.mirror_x, sprite_data.mirror_y, event_subscription)
