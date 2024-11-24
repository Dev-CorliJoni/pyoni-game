from PIL import Image

from pyonigame.models.components.image_data import SpriteData
from pyonigame.components.base import ImageBase
from pyonigame.events import Event


class Sprite(ImageBase):

    def __init__(self, x, y, sprite_data: SpriteData, layer=ImageBase.Layer.GAME_ELEMENT, event_subscription: Event = Event.NONE, scale_factor=1):
        sprite_coordinates = sprite_data.locator_tuple()
        if sprite_data.is_locator_empty():
            width, height = Image.open(sprite_data.image_path).size
            width, height = width * scale_factor, height * scale_factor
            sprite_coordinates = (0, 0, width, height)
        elif sprite_data.is_locator_valid():
            width, height = sprite_coordinates[2] * scale_factor, sprite_coordinates[3] * scale_factor
        else:
            raise ValueError("Sprite data x, y, width and height have to be set or all set to None!")

        super().__init__("sprite", layer, x, y, width, height, sprite_coordinates, sprite_data.image_path,
                         scale_factor, sprite_data.image_rotation, sprite_data.mirror_x, sprite_data.mirror_y, event_subscription)
