from pyonigame.components.base import EventBase, CoordinateBase, ShapeBase
from pyonigame.events import Event


class ImageBase(EventBase, CoordinateBase, ShapeBase):
    """
    Represents base class for an image element.
    """
    def __init__(self, type_, layer, x, y, width, height, sprite_coordinates: tuple[int, int, int, int], image_path, scale_factor, image_rotation, mirror_x, mirror_y, event_subscription: Event):
        """
        :param type_: The type of the game element.
        :param layer: Specifies the hierarchical layer the element belongs to.
               Layers are arranged from back to front as follows: BACKGROUND -> GAME_ELEMENT -> CONTROL.
        :param x: The x-coordinate of the image's position on the UI.
        :param y: The y-coordinate of the image's position on the UI.
        :param width: The width of the image.
        :param height: The height of the image.
        :param image_path: The file path to the image to be displayed.
        :param sprite_coordinates: The x, y, width, height coordinates of the sprite sheet.
        :param scale_factor: The factor by which the image is scaled.
        :param image_rotation: The rotation angle of the image (in degrees).
        :param mirror_x: Whether to mirror the image along the x-axis (True or False).
        :param mirror_y: Whether to mirror the image along the y-axis (True or False).
        :param event_subscription: Defines the events that the object will subscribe to
        """
        super().__init__(type_, layer, event_subscription)
        CoordinateBase.__init__(self, x, y)
        ShapeBase.__init__(self, width, height)

        self.path = image_path
        self.sprite_coordinates = sprite_coordinates

        self.image_scale = scale_factor
        self.image_rotation = image_rotation
        self.image_mirrored_x = mirror_x
        self.image_mirrored_y = mirror_y
