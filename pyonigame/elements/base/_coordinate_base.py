class CoordinateBase:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, dx, dy):
        self.x += dx
        self.y += dy

    def set(self, x, y):
        self.x = x
        self.y = y

    def get_coordinates_by_percentage(self, dimension, x_percentage, y_percentage, width, height):
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
