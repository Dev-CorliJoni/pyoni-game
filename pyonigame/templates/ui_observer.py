from abc import ABC, abstractmethod
from typing import Generator

from pyonigame.events import Request
from pyonigame.models import DictObject


class Observer(ABC):

    def __init__(self) -> None:
        self.opened: bool = False

    @abstractmethod
    def apply_settings(self, settings: DictObject) -> None:
        pass

    @abstractmethod
    def get_inputs(self) -> Generator[DictObject, None, None]:
        pass

    @abstractmethod
    def update(self, requests: list[Request], updates: list[DictObject]) -> None:
        pass
