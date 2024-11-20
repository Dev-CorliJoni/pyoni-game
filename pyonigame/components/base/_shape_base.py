class ShapeBase:
    """
    Represents base class for managing shape data (width, height).
    """

    def __init__(self, width=float('nan'), height=float('nan')):
        """
        :param width: The initial width of the shape.
        :param height: The initial height of the shape.
        """
        self.width = width
        self.height = height

    def resize(self, width, height):
        """
        :param width: The new width of the shape.
        :param height: The new height of the shape.
        """
        self.width = width
        self.height = height
