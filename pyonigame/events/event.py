from enum import Flag, auto


class Event(Flag):
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
