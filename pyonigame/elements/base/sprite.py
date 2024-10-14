from pyonigame.elements.base import ImageBase
from PIL import Image


class Sprite(ImageBase):

    def __init__(self, image_path, x, y, sprite_coordinates=None, layer=ImageBase.Layer.GAME_ELEMENT, scale_factor=1, image_rotation=0, mirror_x=False, mirror_y=False, click_event=None):
        if sprite_coordinates is None:
            width, height = Image.open(image_path).size
            width, height = width * scale_factor, height * scale_factor
            self.sprite_coordinates = (0, 0, width, height)
        else:
            width, height = sprite_coordinates[2] * scale_factor, sprite_coordinates[3] * scale_factor
            self.sprite_coordinates = sprite_coordinates

        super().__init__("sprite", layer, image_path, x, y, width, height, scale_factor, image_rotation, mirror_x, mirror_y, click_event)
