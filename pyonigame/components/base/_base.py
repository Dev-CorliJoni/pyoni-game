from enum import Enum

from pyonigame.models import DictObject


class Base:
    COUNTER = 0

    class Layer(Enum):
        BACKGROUND = "background"
        GAME_ELEMENT = "game_element"
        CONTROL = "control"

    def __init__(self, type_: str, layer: Layer):
        self.id = Base.COUNTER
        self.type = type_
        self.layer = layer
        self.state_changed = True

        Base.COUNTER += 1

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        if key != 'state_changed' and not key.startswith('_'):
            self.state_changed = True

    def update(self, passed_time, post_change_func=lambda: None):
        post_change_func()

        vars_ = vars(self)
        obj = DictObject({key: vars_[key] for key in vars_ if not key.startswith("_") and key == key.lower()})
        obj.layer = self.layer.value

        self.state_changed = False
        return obj
