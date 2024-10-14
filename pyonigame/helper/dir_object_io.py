import json
from pyonigame.helper import DirObject


class DirObjectIO:
    def __init__(self, path):
        self.path = path

    def load(self):
        with open(self.path, "r") as f:
            dir_object = DirObject(json.load(f))
        return dir_object

    def write(self, dir_object: DirObject):
        with open(self.path, "w") as f:
            f.write(json.dumps(dir_object.to_dict(), indent=4))
