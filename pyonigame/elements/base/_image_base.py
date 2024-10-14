from pyonigame.elements.base import ClickableBase


class ImageBase(ClickableBase):
    def __init__(self, type_, layer, image_path, x, y, width, height, scale_factor, image_rotation, mirror_x, mirror_y, click_event):
        super().__init__(type_, layer, x, y, width, height, click_event)

        self.path = image_path

        self.image_scale = scale_factor
        self.image_rotation = image_rotation
        self.image_mirrored_x = mirror_x
        self.image_mirrored_y = mirror_y
