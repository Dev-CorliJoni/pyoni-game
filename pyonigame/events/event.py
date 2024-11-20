from enum import Flag, auto


class Event(Flag):
    """
    The following events are supported:
        - `Event.THEME_CHANGED`: Triggers the `EventBase.theme_changed` method.
        - `Event.LANGUAGE_CHANGED`: Triggers the `EventBase.language_changed` method.
        - `Event.SCREEN_SIZE_CHANGED`: Triggers the `EventBase.screen_size_changed` method.
        - `Event.KEY`: Triggers the `EventBase.key_press` and `EventBase.key_release` methods.
        - `Event.MOUSE`: Triggers the `EventBase.left_click`, `EventBase.middle_click`, `EventBase.right_click`,
                         `EventBase.hover`, `EventBase.scroll_up`, and `EventBase.scroll_down` methods.
        - `Event.FOCUS`: Triggers the `EventBase.focus` and `EventBase.lost_focus` methods.
        - `Event.DRAG_AND_DROP`: Triggers the `EventBase.drag_start`, `EventBase.dragging`, and `EventBase.drop` methods.
        - `Event.COLLISION`: Not yet implemented.
    """
    NONE = 0

    THEME_CHANGED = auto()
    LANGUAGE_CHANGED = auto()
    SCREEN_SIZE_CHANGED = auto()
    KEY = auto()
    MOUSE = auto()
    FOCUS = auto()
    DRAG_AND_DROP = auto()
    COLLISION = auto()

    ALL = THEME_CHANGED | LANGUAGE_CHANGED | SCREEN_SIZE_CHANGED | KEY | MOUSE | FOCUS | DRAG_AND_DROP | COLLISION
