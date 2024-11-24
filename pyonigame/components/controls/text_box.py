from functools import partial

from pyonigame.components.core import Rect, Text
from pyonigame.models.components.validators import StringValidator


class Style:

    DEFAULT_PADDING = 10

    def __init__(self, font, size, bg_color, text_color, border_color, padding=DEFAULT_PADDING, border_radius=10):
        self.font = font
        self.size = size
        self.background_color = bg_color
        self.text_color = text_color
        self.border_color = border_color
        self.padding = padding
        self.border_radius = border_radius

    @staticmethod
    def default(font, size, **kwargs):
        return Style(font, size, (255, 255, 255), (0, 0, 0), (0, 0, 0), **kwargs)

    @staticmethod
    def setting(font, size, **kwargs):
        return Style(font, size, (255, 255, 255), (0, 0, 0), (128, 0, 32), **kwargs)


class Key:

    def __init__(self, unicode, value):
        self.unicode = unicode
        self.value = value

        self.is_processed = False
        self.is_released = False


def is_key_match(pressed, released):
    return released != "" and released in (pressed.upper(), pressed.lower())


class TextBox(Rect):

    BLINK_INTERVAL = 0.5
    KEY_PRESS_INTERVAL = 0.3

    def __init__(self, x, y, width, height, style, get_font_dimension, validator=StringValidator(), enter_func=lambda _: None, text="", hint="", layer=Rect.Layer.CONTROL, select_key_mode=False):
        super().__init__(x, y, width, height, style.background_color, border_color=style.border_color, layer=layer, border_radius=style.border_radius, click_event=self.focus)
        self.lost_focus_event = self.lost_focus
        self._validator = validator
        self._is_valid = True
        self._select_key_mode = select_key_mode

        self._enter_func = enter_func
        self._get_font_dimension = get_font_dimension

        self._cursor_blink_time = TextBox.BLINK_INTERVAL
        self._key_press_time = 0

        self._current_key_pressed_interval = TextBox.KEY_PRESS_INTERVAL
        self._pressed_keys = []
        self._cursor_right = False
        self._cursor_left = False
        self._backspace = False
        self._delete = False

        self._style = style
        self._padded_x_start = 0
        self._padded_x_end = 0
        self._padded_width = 0
        self._text_str = text
        self._hint = hint
        self.set_padding(style.padding, False)

        self._text = Text(text, style.font, style.size, style.text_color, self._padded_x_start, 0, get_font_dimension, layer=layer)
        self._text.y = int(y + (height - self._text.height) / 2)
        self._cursor = Rect(x, self._text.y + self._text.height * 0.05, 2, self._text.height * 0.9, style.text_color, layer=layer)

        self._active = False
        self._is_editable = True
        self._cursor_visible = False

        self._scroll_offset = 0  # Initialize the scroll offset to 0 at the start
        self._cursor_index = 0

        self.set_cursor(0, False)

    @property
    def is_editable(self):
        return self._is_editable

    @is_editable.setter
    def is_editable(self, is_editable):
        self._is_editable = is_editable

    @property
    def is_valid(self):
        return self._is_valid

    def set(self, x, y):
        super().set(x, y)
        self.set_padding(self._style.padding, set_tb=False)
        self._text.set(self._padded_x_start, int(y + (self.height - self._text.height) / 2))
        self._cursor.set(self._cursor.x, self._text.y + self._text.height * 0.05)

    def resize(self, width, height):
        super().resize(width, height)
        self.set_padding(self._style.padding, set_tb=False)
        self._text.resize(self._padded_width, self.height - (self.height * 0.05))
        self._cursor.resize(2, self._text.height * 0.9)

    def set_padding(self, padding, set_tb=True):
        padding = max(self._style.padding, padding)
        self._padded_x_start = self.x + padding
        self._padded_x_end = self.x + self.width - padding
        self._padded_width = self.width - padding * 2
        if set_tb:
            self._text.x = self._padded_x_start

    def get_text_width(self, text):
        return self._get_font_dimension(text, self._text.font, self._text.size)[0]

    def set_text(self, new_text):
        self._text_str = new_text
        self._text.text = new_text
        self._text.calculate_size()
        self._scroll_offset = 0  # Reset scroll offset when the text changes

    def lost_focus(self):
        self._active = False
        self.state_changed = True

    def focus(self, pos):
        if self.x < pos[0] < self.x + self.width and self.is_editable:
            self._active = True
            relative_x = pos[0] - self._padded_x_start
            if self._text.text not in self._text_str:
                self.set_cursor(0)
            else:
                new_rel_index = self.get_index_from_text_point(relative_x)
                self.set_cursor(new_rel_index + self._text_str.index(self._text.text))

    def get_index_from_text_point(self, value):
        # Connect index and text_width and find in the next step the nearest value to relative_x
        text_info = [(i, self.get_text_width(self._text.text[:i])) for i in range(len(self._text.text) + 1)]
        nearest_item = min(text_info, key=lambda i: abs(i[1] - value))
        return nearest_item[0]

    def set_cursor(self, cursor_index, change_cursor_blink_state=True):
        self._cursor_index = min(int(cursor_index), len(self._text_str))
        self._cursor_index = max(self._cursor_index, 0)

        self._text.text, rel_index = self.get_visible_text(self._cursor_index)
        width = self.get_text_width(self._text.text[:rel_index])
        self._cursor.set(self._text.x + width, self._cursor.y)
        self.change_cursor_blink_state(change_cursor_blink_state)

    def get_visible_text(self, cursor_index):
        text_width = self.get_text_width(self._text_str)
        cut_text_width = self.get_text_width(self._text_str[:cursor_index + 1])

        # If the text fits within the padded width, return the full string
        if text_width <= self._padded_width:
            return self._text_str, cursor_index

        half_box_width = self._padded_width // 2

        # Only adjust the start index if the cursor moves too far left or right
        if cut_text_width < self._scroll_offset:
            # Cursor is too far to the left, move the visible text left
            self._scroll_offset = max(0, cut_text_width - half_box_width)
        elif cut_text_width > self._scroll_offset + self._padded_width:
            # Cursor is too far to the right, move the visible text right
            self._scroll_offset = cut_text_width - self._padded_width + half_box_width

        # Now determine the visible portion of text based on the scroll offset
        start_index = 0
        visible_text = ""
        total_width = 0

        for i, char in enumerate(self._text_str):
            char_width = self.get_text_width(char)
            total_width += char_width

            if total_width > self._scroll_offset:
                start_index = i
                break

        total_width = 0
        for i in range(start_index, len(self._text_str)):
            char = self._text_str[i]
            total_width += self.get_text_width(char)
            if total_width > self._padded_width:
                break
            visible_text += char

        relative_cursor_index = cursor_index - start_index
        return visible_text, relative_cursor_index

    def change_cursor_blink_state(self, state):
        self._cursor_blink_time = TextBox.BLINK_INTERVAL
        self._cursor_visible = state
        self.state_changed = True

    def update(self, inputs, post_change_func=lambda: None):
        passed_time = float(next(filter(lambda i: i.type == "passed_time", inputs)).value)

        if self._cursor_blink_time < passed_time and self.is_editable and self._active:
            self.change_cursor_blink_state(not self._cursor_visible)

        if self._active and self.is_editable:
            self._cursor_blink_time -= passed_time

            all_key_events = filter(lambda i: i.type in ("key", "key_end"), inputs)

            for input_ in all_key_events:
                if input_.second_value == "p2_right" and self._select_key_mode is False:
                    self._cursor_right = input_.type == "key"
                elif input_.second_value == "p2_left" and self._select_key_mode is False:
                    self._cursor_left = input_.type == "key"
                elif input_.value == "backspace" and self._select_key_mode is False:
                    self._backspace = input_.type == "key"
                elif input_.value == "delete" and self._select_key_mode is False:
                    self._delete = input_.type == "key"
                elif input_.value == "return" and input_.type == "key" and self._select_key_mode is False:
                    if self._validator.validate(self._text_str):
                        self._enter_func(self._text_str)
                elif input_.type == "key" and (self._select_key_mode or (len(input_.unicode) == 1 and input_.unicode.isprintable())):
                    self._pressed_keys.append(Key(input_.unicode, input_.value))
                elif input_.type == "key_end" and (self._select_key_mode or (len(input_.unicode) == 1 and input_.unicode.isprintable())):
                    key = next(filter(lambda k: (is_key_match(k.value, input_.value) or is_key_match(k.unicode, input_.unicode)) and not k.is_released, self._pressed_keys), None)
                    if key is not None:
                        key.is_released = True

            self.process_inputs(passed_time)

        if self._text_str == "" and self._hint != "":
            self._text.text = self._hint
            self._text.calculate_size()

        rect_update = super().update(inputs, post_change_func=partial(self._update_states, post_change_func))
        updates = [rect_update, self._text.update(inputs)]
        if self._cursor.state_changed:
            updates.append(self._cursor.update(inputs))

        return updates

    def process_inputs(self, passed_time):
        is_key_pressed = len(self._pressed_keys) > 0
        is_next_key_event = self._key_press_time - passed_time < 0

        if self._cursor_right and is_next_key_event:
            self.set_cursor(min(self._cursor_index + 1, len(self._text_str)))
        elif self._cursor_left and is_next_key_event:
            self.set_cursor(max(self._cursor_index - 1, 0))
        elif self._backspace and is_next_key_event:
            removed_index = max(self._cursor_index - 1, 0)
            self.set_text(f"{self._text_str[:removed_index]}{self._text_str[self._cursor_index:]}")
            self.set_cursor(self._cursor_index - 1)
        elif self._delete and is_next_key_event:
            self.set_text(f"{self._text_str[:self._cursor_index]}{self._text_str[self._cursor_index + 1:]}")
            self.set_cursor(self._cursor_index)
        elif is_key_pressed:
            for key in self._pressed_keys[:]:
                if not key.is_processed or (is_next_key_event and not key.is_released):
                    if self._select_key_mode:
                        text = f"{key.value}"
                        self._cursor_index = len(text)
                        if self._validator.validate(text):
                            self._enter_func(text)
                    else:
                        text = f"{self._text_str[:self._cursor_index]}{key.unicode}{self._text_str[self._cursor_index:]}"
                        self._cursor_index = self._cursor_index + 1

                    self.set_text(text)
                    self.set_cursor(self._cursor_index)
                    key.is_processed = True

                if key.is_processed and key.is_released:
                    self._pressed_keys.remove(key)

        self.handle_key_press(passed_time, is_next_key_event, is_key_pressed)

        self._is_valid = self._validator.validate(self._text_str)
        self.set_validation_color()

    def handle_key_press(self, passed_time, is_next_key_event, is_key_pressed):
        if self._cursor_left or self._cursor_right or self._backspace or self._delete or is_key_pressed:
            if is_next_key_event:
                self._key_press_time = self._current_key_pressed_interval
                self._current_key_pressed_interval = max(self._current_key_pressed_interval * 0.85, 0.05)
            else:
                self._key_press_time -= passed_time

        if not any((self._cursor_left, self._cursor_right, self._backspace, self._delete, is_key_pressed)):
            self._key_press_time = 0
            self._current_key_pressed_interval = TextBox.KEY_PRESS_INTERVAL

    def set_validation_color(self):
        if self._is_valid or self._text_str == "":
            self.border_color = self._style.border_color
        else:
            self.border_color = (255, 0, 0)

    def _update_states(self, post_change_func):
        self._text.state_changed = self.state_changed or self._text.state_changed
        self._cursor.state_changed = self._active and self._cursor_visible
        post_change_func()
