class ShapeBase:
    def __init__(self, width=float('nan'), height=float('nan')):
        self.width = width
        self.height = height

    def resize(self, width, height):
        self.width = width
        self.height = height
