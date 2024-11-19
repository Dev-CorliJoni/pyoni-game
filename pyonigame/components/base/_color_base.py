from typing import Union


class ColorBase:
    def __init__(self, color: Union[tuple[float, float, float], str]):
        self.color = color

    def set_color(self, color):
        self.color = color
