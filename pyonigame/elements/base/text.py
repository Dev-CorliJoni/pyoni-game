from pyonigame.elements.base import ClickableBase, ColorBase


class Text(ClickableBase, ColorBase):

    ARIAL = "arial"
    CINZEL = "cinzel"
    CINZEL_BOLD = "cinzel-bold"

    def __init__(self, text, font, size, color: tuple[float, float, float], x, y, get_font_dimension, layer=ClickableBase.Layer.CONTROL, bold=False, click_event=None):
        self._get_font_dimension = get_font_dimension
        width, height = self._get_font_dimension(text, font, size)

        super().__init__("text", layer, x, y, width, height, click_event)
        ColorBase.__init__(self, color=color)

        self.text = text
        self.font = font
        self._max_size = size
        self.size = size
        self.bold = bold
        self.calculate_size()

    def calculate_size(self):
        self.width, self.height = self._get_font_dimension(self.text, self.font, self.size)

    def resize(self, width, height):
        self.size = self._max_size
        self.calculate_size()
        while self.size > 1:
            if self.width <= width and self.height <= height:
                break

            self.size -= 1
            self.calculate_size()
