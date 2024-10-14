from pyonigame.elements.controls import Button, ButtonStyle


class Style(ButtonStyle):
    def __init__(self, font, size, bg_color, active_bg_color, text_color, border_color=(0, 0, 0), padding=20, border_radius=10, border_width=5):
        super().__init__(font, size, bg_color, active_bg_color, text_color, border_color, border_radius, border_width)
        self.padding = padding

    @staticmethod
    def on_gras(font, size, **kwargs):
        return Style(font, size, (139, 69, 19), (128, 0, 32), (200, 200, 200), (205, 133, 63), **kwargs)


class AlignableButton(Button):

    def __init__(self, text, x_percentage, y_percentage, height_percentage, style, get_font_dimension, get_dimension, click_event, layer=Button.Layer.CONTROL):
        super().__init__(text, 0, 0, 0, 0, style, get_font_dimension, get_dimension, click_event, layer, x_percentage, y_percentage, height_percentage)

    def update(self, inputs, **kwargs):
        self.set_text_form()
        self.set_coordinates()
        return super().update(inputs, **kwargs)
