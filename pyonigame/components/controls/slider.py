from functools import partial
from pyonigame.components.controls import Text, TextBox, TextBoxStyle, Button, ButtonStyle
from models.components.validators import StringValidator


class Style(TextBoxStyle):

    def __init__(self, font, size, bg_color, text_color, border_color, padding=TextBoxStyle.DEFAULT_PADDING, border_radius=10):
        super().__init__(font, size, bg_color, text_color, border_color, padding, border_radius)

    @staticmethod
    def default(font, size, **kwargs):
        return Style(font, size, (255, 255, 255), (0, 0, 0), (0, 0, 0), **kwargs)

    @staticmethod
    def setting(font, size, **kwargs):
        return Style(font, size, (255, 255, 255), (0, 0, 0), (128, 0, 32), **kwargs)


class Slider(TextBox):

    def __init__(self, texts, x, y, width, height, style, get_font_dimension, get_dimension, value_changed_func, validator=StringValidator(), is_editable=False, centered=True, hint="", slider_index=0, layer=TextBox.Layer.CONTROL):
        self._slider_index = slider_index
        self._texts = dict(enumerate(texts))
        super().__init__(x, y, width, height, style, get_font_dimension, validator, enter_func=value_changed_func, text=self.current_text, hint=hint, layer=layer)

        on_hover_color = (style.background_color[0] * 0.85, style.background_color[1] * 0.85, style.background_color[2] * 0.85)
        style = ButtonStyle(Text.ARIAL, 30, style.background_color, on_hover_color, style.text_color, border_width=0)
        t_width = get_font_dimension("◄", style.font, style.size)[0] + 5
        self.is_editable = is_editable
        self._is_centered = centered
        self.value_changed_func = value_changed_func

        self._buttons = [
            Button("◄", 0, 0, 0, 0, style, get_font_dimension, get_dimension, click_event=lambda _: self.adj_slider_index(-1), layer=layer),
            Button("►", 0, 0, 0, 0, style, get_font_dimension, get_dimension, click_event=lambda _: self.adj_slider_index(1), layer=layer),
        ]

        self.buttons_resize((t_width, height), (t_width, height))
        self.buttons_set((x, y), (x + self.width - self._buttons[1].width, y))

        self.align_text()

    @property
    def current_text(self):
        self._slider_index = (self._slider_index + len(self._texts)) % len(self._texts)
        return self._texts[self._slider_index]

    def buttons_set(self, *coordinates):
        for i, button in enumerate(self._buttons):
            button.set(*coordinates[i])

    def buttons_resize(self, *shape_data):
        for i, button in enumerate(self._buttons):
            button.resize(*shape_data[i], adjust_over_text_height=True)

    def set(self, x, y):
        super().set(x, y)
        self.align_text()
        self.buttons_set((x, y), (x + self.width - self._buttons[1].width, y))

    def resize(self, width, height):
        super().resize(width, height)
        self.buttons_resize((self._buttons[0].width, height), (self._buttons[1].width, height))

    def focus(self, pos):
        if self.x + self._buttons[0].width < pos[0] < self.x + self.width - self._buttons[0].width:
            super().focus(pos)

    def align_text(self):
        if self._is_centered:
            padding = max((self.width - self._text.width) // 2, self._buttons[0].width + Style.DEFAULT_PADDING)
            self.set_padding(padding)
        else:
            self.set_padding(self._buttons[0].width + Style.DEFAULT_PADDING)

    def set_text(self, text):
        super().set_text(text)
        self.align_text()

    def adj_slider_index(self, change):
        self._slider_index = self._slider_index + change

        self.set_text(self.current_text)
        self.set_cursor(0)
        self._is_valid = self._validator.validate(self._text_str)
        self.set_validation_color()

        self._active = False
        self.state_changed = True
        if self._validator.validate(self._text_str):
            self.value_changed_func(self.current_text)

    def update(self, inputs, post_change_func=lambda: None):
        tb_updates = super().update(inputs, post_change_func=partial(self._update_button_states, post_change_func))
        return [*tb_updates, *[update for b in self._buttons for update in b.update(inputs)]]

    def _update_button_states(self, post_change_func):
        if self._text.text == self._hint:
            self.align_text()

        for button in self._buttons:
            button.any_state_changed = button.any_state_changed or self.state_changed
        post_change_func()
