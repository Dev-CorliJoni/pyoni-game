from pyonigame.helper import DictObject


class Base:
    counter = 0

    class Layer:
        BACKGROUND = "background"
        GAME_ELEMENT = "game_element"
        CONTROL = "control"

    def __init__(self, type_: str, layer: str):
        self.id = Base.counter
        self.type = type_
        self.layer = layer
        self.state_changed = True

        Base.counter += 1

    def __setattr__(self, key, value):
        super().__setattr__(key, value)
        if key != 'state_changed' and not key.startswith('_'):
            self.state_changed = True

    def update(self, inputs, post_change_func=lambda: None):
        post_change_func()

        vars_ = vars(self)
        obj = DictObject({key: vars_[key] for key in vars_ if not key.startswith("_") and key == key.lower()})
        self.state_changed = False
        return obj
