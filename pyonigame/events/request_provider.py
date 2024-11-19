from pyonigame.events import ApplicationManager, RequestType, Request
from pyonigame.models import DictObject
from pyonigame.models.settings import Settings


class RequestProvider:

    def quit(self):
        return ApplicationManager.request(Request(RequestType.QUIT, DictObject()), self)

    def refresh(self):
        return ApplicationManager.request(Request(RequestType.REFRESH, DictObject()), self)

    def refresh_settings(self, settings: Settings):
        return ApplicationManager.request(Request(RequestType.REFRESH_SETTINGS, settings), self)

    @property
    def settings(self) -> Settings:
        return ApplicationManager.SETTINGS.copy()
