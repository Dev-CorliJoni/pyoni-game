import json
from enum import Enum
from pyonigame.models import DictObject


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Enum):
            return obj.value
        return super().default(obj)


class IODictObject:
    def __init__(self, path):
        self.path = path

    def load(self) -> DictObject:
        with open(self.path, "r") as f:
            dict_object = DictObject(json.load(f))
        return dict_object

    def write(self, dict_object: DictObject):
        with open(self.path, "w") as f:
            f.write(json.dumps(dict_object.to_dict(), indent=4, cls=CustomEncoder))
