from pyonigame.components.base import Base, CoordinateBase, ShapeBase


class ClickableBase(Base, CoordinateBase, ShapeBase):

    def __init__(self, type_, layer, x, y, width, height, click_event):
        super().__init__(type_, layer)
        CoordinateBase.__init__(self, x=x, y=y)
        ShapeBase.__init__(self, width=width, height=height)

        self._clicked_position = (-1, -1)
        self.left_click_event = click_event
        self.middle_click_event, self.right_click_event, self.scroll_up_event, self.scroll_down_event, self.lost_focus_event = (None,) * 5

    @property
    def clickable(self):
        return self._left_mouse_clickable or self._middle_mouse_clickable or self._right_mouse_clickable or self.scroll_up_event or self.scroll_down_event

    @property
    def left_click_event(self):
        return self._left_click_event

    @left_click_event.setter
    def left_click_event(self, value):
        self._left_mouse_clickable, self._left_click_event = value is not None, value

    @property
    def middle_click_event(self):
        return self._middle_click_event

    @middle_click_event.setter
    def middle_click_event(self, value):
        self._middle_mouse_clickable, self._middle_click_event = value is not None, value

    @property
    def right_click_event(self):
        return self._right_click_event

    @right_click_event.setter
    def right_click_event(self, value):
        self._right_mouse_clickable, self._right_click_event = value is not None, value

    @property
    def lost_focus_event(self):
        return self._lost_focus_event

    @lost_focus_event.setter
    def lost_focus_event(self, value):
        self._can_lost_focus, self._lost_focus_event = value is not None, value

    @property
    def scroll_up_event(self):
        return self._scroll_up_event

    @scroll_up_event.setter
    def scroll_up_event(self, value):
        self._can_scroll_up, self._scroll_up_event = value is not None, value

    @property
    def scroll_down_event(self):
        return self._scroll_down_event

    @scroll_down_event.setter
    def scroll_down_event(self, value):
        self._can_scroll_down, self._scroll_down_event = value is not None, value

    def _lost_focus(self):
        if self._can_lost_focus:
            self._lost_focus_event()

    def _clicked(self, pos, button):
        if button == "left" and self._left_mouse_clickable:
            self._clicked_position = pos
            self.left_click_event(pos)
        elif button == "middle" and self._middle_mouse_clickable:
            self._clicked_position = pos
            self.middle_click_event(pos)
        elif button == "right" and self._right_mouse_clickable:
            self._clicked_position = pos
            self.right_click_event(pos)

    def _scroll(self, value):
        if value == "up" and self._can_scroll_up:
            self.scroll_up_event()
        elif value == "down" and self._can_scroll_down:
            self.scroll_down_event()

    def update(self, inputs, post_change_func=lambda: None):
        if self.clickable:
            clicked = next(filter(lambda i: i.type == "click" and i.id == self.id, inputs), None)
            clicked_pos = clicked.pos if clicked is not None else (-1, -1)
            scroll = next(filter(lambda i: i.type == "scroll" and i.id == self.id, inputs), None)
            lost_focus = next(filter(lambda i: i.type == "click" and i.id != self.id and i.pos != clicked_pos, inputs), None)

            if clicked is not None:
                self._clicked(clicked.pos, clicked.button)
            if scroll is not None:
                self._scroll(scroll.value)
            if lost_focus is not None and lost_focus.pos != self._clicked_position:
                self._lost_focus()

        return super().update(inputs, post_change_func)

    def _simulate_click(self, is_clickable, click_event):
        if is_clickable:
            self._clicked_position = (self.x, self.y)
            click_event(self._clicked_position)

    def simulate_left_click(self):
        self._simulate_click(self._left_mouse_clickable, self.left_click_event)

    def simulate_middle_click(self):
        self._simulate_click(self._middle_mouse_clickable, self.middle_click_event)

    def simulate_right_click(self):
        self._simulate_click(self._right_mouse_clickable, self.right_click_event)
