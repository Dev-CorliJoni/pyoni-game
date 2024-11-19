from pyonigame.components.event_communication import ParentComponent


def child_component(cls):
    old_constructor = cls.__init__

    def constructor(self, parent: ParentComponent, *args, **kwargs):
        self._parent = parent
        old_constructor(self, *args, **kwargs)

    cls.__init__ = constructor

    cls.theme_changed = lambda self, theme: self._parent.theme_changed(self, theme)
    cls.language_changed = lambda self, language: self._parent.language_changed(self, language)
    cls.screen_size_changed = lambda self, width, height: self._parent.screen_size_changed(self, width, height)

    cls.left_click = lambda self, mouse_x, mouse_y: self._parent.left_click(self, mouse_x, mouse_y)
    cls.middle_click = lambda self, mouse_x, mouse_y: self._parent.middle_click(self, mouse_x, mouse_y)
    cls.right_click = lambda self, mouse_x, mouse_y: self._parent.right_click(self, mouse_x, mouse_y)
    cls.hover = lambda self, mouse_x, mouse_y: self._parent.hover(self, mouse_x, mouse_y)

    cls.focus = lambda self, mouse_x, mouse_y: self._parent.focus(self, mouse_x, mouse_y)
    cls.lost_focus = lambda self: self._parent.lost_focus(self)

    cls.drag_start = lambda self, mouse_x, mouse_y: self._parent.drag_start(self, mouse_x, mouse_y)
    cls.dragging = lambda self, mouse_x, mouse_y: self._parent.dragging(self, mouse_x, mouse_y)
    cls.drop = lambda self, mouse_x, mouse_y: self._parent.drop(self, mouse_x, mouse_y)

    cls.scroll_up = lambda self: self._parent.scroll_up(self)
    cls.scroll_down = lambda self: self._parent.scroll_down(self)

    cls.key_press = lambda self, unicode, value, mapped_value: self._parent.key_press(self, unicode, value, mapped_value)
    cls.key_release = lambda self, unicode, value, mapped_value: self._parent.key_release(self, unicode, value, mapped_value)

    return cls
