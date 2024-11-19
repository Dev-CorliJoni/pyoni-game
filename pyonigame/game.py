from time import time

from pyonigame.models.settings import Settings
from pyonigame.templates import ContextController, UIObserver
from pyonigame.events.application_manager import ApplicationManager
from pyonigame.ui._subject import Subject


class Game:
    def __init__(self, controller: ContextController, settings: Settings, *observers: UIObserver) -> None:
        self.controller = controller
        ApplicationManager.SETTINGS = settings
        self.subject = Subject(settings.view, *observers)
        self.running = True
        self.last_update_time = time()

    def run(self):
        while self.running:
            inputs = list(self.subject.get_inputs())
            ApplicationManager.process_inputs(inputs)

            updates = self.controller.update(self.get_passed_time())

            requests = list(ApplicationManager.generate_requests())
            self.subject.update(requests, updates)

            self.running = all([r.type != "quit" for r in requests])

    # except Exception as e:
    #    print(repr(e))

    def get_passed_time(self):
        timestamp = time()
        passed_time = timestamp - self.last_update_time
        self.last_update_time = timestamp
        return passed_time
