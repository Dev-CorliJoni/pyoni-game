from pyonigame.models.settings import DisplayDimension


class CoordinateBase:
    """
    Represents a base class for managing 2D coordinates (x, y).
    """

    def __init__(self, x: float, y: float):
        """
        :param x: The initial x-coordinate on the UI.
        :param y: The initial y-coordinate on the UI.
        """
        self.x = x
        self.y = y

    def move(self, dx: float, dy: float):
        """
        Moves the coordinates by the specified deltas.

        :param dx: The amount of pixels to move the x-coordinate on the UI.
        :param dy: The amount of pixels to move the y-coordinate on the UI.
        """
        self.x += dx
        self.y += dy

    def set(self, x: float, y: float):
        """
        Sets the coordinates to the specified values.

        :param x: The new x-coordinate on the UI.
        :param y: The new y-coordinate on the UI.
        """
        self.x = x
        self.y = y

    @staticmethod
    def get_coordinates_by_percentage(dimension: DisplayDimension, x_percentage: float, y_percentage: float, width: float, height: float):
        """
        Calculates coordinates based on percentage positions within given dimensions,
        ensuring the result stays within bounds.

        :param dimension: A 'DisplayDimension', representing the container's dimensions.
        :param x_percentage: The percentage (0.0 to 1.0) of the x-position relative to the container's width.
        :param y_percentage: The percentage (0.0 to 1.0) of the y-position relative to the container's height.
        :param width: The width of the object being positioned.
        :param height: The height of the object being positioned.

        :return: A tuple (x, y) representing the calculated coordinates.
        """
        x = (dimension.width * x_percentage) - (width / 2)
        y = (dimension.height * y_percentage) - (height / 2)

        if dimension.width < x + width + 10:
            x = dimension.width - width - 10

        if dimension.height < y + height + 10:
            y = dimension.height - height - 10

        if 0 > x - 10:
            x = 10

        if 0 > y - 10:
            y = 10

        return x, y
