from enum import Enum

from pyonigame.models import DictObject


class Base:
    """
    Represents the base class for each derived element in the game with a unique ID, type, and layer.
    Tracks state changes for efficient updates.
    """
    COUNTER = 0

    class Layer(Enum):
        """
        Defines the possible layers of the UI in hierarchical order.
        Layers are arranged from back to front as follows: BACKGROUND -> GAME_ELEMENT -> CONTROL.
        """

        BACKGROUND = "background"
        GAME_ELEMENT = "game_element"
        CONTROL = "control"

    def __init__(self, type_: str, layer: Layer):
        """
        :param type_: The type of the game element.
        :param layer: Specifies the hierarchical layer the element belongs to.
               Layers are arranged from back to front as follows: BACKGROUND -> GAME_ELEMENT -> CONTROL.
        """
        self.id = Base.COUNTER
        self.type = type_
        self.layer = layer
        self.state_changed = True

        Base.COUNTER += 1

    def __setattr__(self, key, value):
        """
        Sets an attribute and marks the object as changed if the attribute
        is not 'state_changed' and does not start with an underscore.
        """
        super().__setattr__(key, value)
        if key != 'state_changed' and not key.startswith('_'):
            self.state_changed = True

    def update(self, passed_time, post_change_func=lambda: None):
        """
        Updates the object and generates a DictObject representation of its state.

        :param passed_time: The time the object was updated.
        :param post_change_func: Optional function executed right before the object representation is generated.

        :return : A DictObject representation of the object.
        """
        post_change_func()

        vars_ = vars(self)
        obj = DictObject({key: vars_[key] for key in vars_ if not key.startswith("_") and key == key.lower()})
        obj.layer = self.layer.value

        self.state_changed = False
        return obj
