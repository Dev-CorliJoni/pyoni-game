from typing import Union


class ListValidator:
    def __init__(self, list_: Union[list[str], tuple[str]]):
        self._list = list_

    def validate(self, value: str) -> bool:
        return value in self._list
