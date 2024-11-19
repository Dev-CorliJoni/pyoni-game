from functools import partial

from pyonigame.components.controls import AdvancedText, AdvancedTextStyle


class Style(AdvancedTextStyle):
    def __init__(self, font, size, bg_color, active_bg_color, text_color, border_color=(0, 0, 0), border_radius=10, border_width=5, padding=5):
        super().__init__(font, size, bg_color, text_color, border_color, padding, border_radius, border_width)
        self.active_background_color = active_bg_color

    @staticmethod
    def for_slider(font, size, **kwargs):
        return Style(font, size, (255, 255, 255), (220, 220, 220), (0, 0, 0), border_width=0, **kwargs)


class Button(AdvancedText):

    # x-percent and y_percent are just passed for the sake of being the base class for alignable button
    def __init__(self, text, x, y, width, height, style, get_font_dimension, get_dimension, click_event, layer=AdvancedText.Layer.CONTROL, _x_percent=0, _y_percent=0, _height_percent=0):
        super().__init__(text, style, _x_percent, _y_percent, _height_percent, get_font_dimension, get_dimension, layer=layer)

        self.active = False
        self.rect.left_click_event = click_event
        if _height_percent == 0:
            self.resize(width, height)
        if _x_percent == 0 and _y_percent == 0:
            self.set(x, y)

    def update(self, inputs, **kwargs):
        hovering = self.process_inputs(inputs)
        return [self.rect.update(inputs, partial(self.post_update, hovering)), self.text.update(inputs, supress_coordinate_reset=True, **kwargs)]

    def post_update(self, hovering):
        self.process_changes(hovering)
        self.text.state_changed = self.text.state_changed or self.rect.state_changed

    def set(self, x, y):
        self.rect.set(x, y)

        self.text.x = x + (self.width - self.text.width) // 2
        self.text.y = y + (self.height - self.text.height) // 2

    def resize(self, width, height, adjust_over_text_height=False):
        if adjust_over_text_height:
            self.text.resize(width + 20, height - self.style.padding)
            self.rect.resize(self.text.width + self.style.padding, height)
        else:
            self.rect.resize(width, height)
            self.text.resize(width - self.style.padding, height - self.style.padding)

    def process_inputs(self, inputs):
        hovering = False
        for input_ in filter(lambda i: i.type in ("key", "hover"), inputs):
            if input_.type == "key":
                if input_.value == "return" and self.active:  # enter
                    self.rect.simulate_left_click()
            if input_.type == "hover":
                if input_.id == self.rect.id:
                    hovering = True
        return hovering

    def process_changes(self, hovering):
        if hovering and self.rect.color != tuple(min(val + 10, 255) for val in self.style.active_background_color):
            self.rect.color = [min(val + 10, 255) for val in self.style.active_background_color]
        elif self.active:
            self.rect.color = self.style.active_background_color
        elif self.rect.color != self.style.background_color:
            self.rect.color = self.style.background_color
