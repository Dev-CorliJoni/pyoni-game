from pyonigame.elements.base import EventBase, CoordinateBase, ShapeBase
from pyonigame.events import Event


class ImageBase(EventBase, CoordinateBase, ShapeBase):
    def __init__(self, type_, layer, image_path, x, y, width, height, scale_factor, image_rotation, mirror_x, mirror_y, event_subscription: Event):
        super().__init__(type_, layer, event_subscription)
        CoordinateBase.__init__(self, x, y)
        ShapeBase.__init__(self, width, height)

        self.path = image_path

        self.image_scale = scale_factor
        self.image_rotation = image_rotation
        self.image_mirrored_x = mirror_x
        self.image_mirrored_y = mirror_y
