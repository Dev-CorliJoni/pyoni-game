from abc import ABC, abstractmethod

from pyonigame.events import EventController, Request
from pyonigame.models import DictObject


class ContextController(ABC):

    def quit(self):
        EventController.request(Request.quit(), self)

    def refresh(self):
        EventController.request(Request.refresh(), self)

    def refresh_settings(self):
        EventController.request(Request.refresh_settings(), self)

    @abstractmethod
    def update(self, passed_time: float) -> list[DictObject]:
        pass
