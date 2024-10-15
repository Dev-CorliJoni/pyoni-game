import json
from pyonigame.helper import DictObject


class IODictObject:
    def __init__(self, path):
        self.path = path

    def load(self):
        with open(self.path, "r") as f:
            dir_object = DictObject(json.load(f))
        return dir_object

    def write(self, dir_object: DictObject):
        with open(self.path, "w") as f:
            f.write(json.dumps(dir_object.to_dict(), indent=4))
