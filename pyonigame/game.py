from time import time
from pyonigame.helper import DictObject
from pyonigame.view.subject import Subject


class Game:
    def __init__(self, controller, *observers):
        self.controller = controller
        self.subject = Subject(*observers)
        self.running = True
        self.last_update_time = time()

    def run(self):
        # try:
        while self.running:
            inputs = list(self.subject.get_inputs())
            inputs.insert(0, DictObject(type="passed_time", value=f"{self.get_passed_time()}"))

            updates = self.controller.update([i for i in inputs if i is not None])
            self.subject.update(updates)

            self.running = all([i is not None for i in inputs])

    # except Exception as e:
    #    print(repr(e))

    def get_passed_time(self):
        timestamp = time()
        passed_time = timestamp - self.last_update_time
        self.last_update_time = timestamp
        return passed_time
