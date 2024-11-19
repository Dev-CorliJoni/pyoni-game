from abc import ABC, abstractmethod

from pyonigame.events import RequestProvider
from pyonigame.models import DictObject


class ContextController(ABC, RequestProvider):

    @abstractmethod
    def update(self, passed_time: float) -> list[DictObject]:
        pass
