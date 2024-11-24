from models.components.validators.regex_validator import _is_int


class IntValidator:
    def __init__(self, range_: tuple[float, float] = ()):
        self.range_ = range_
        self.has_range = len(range_) == 2

    @property
    def range(self) -> tuple[float, float]:
        return self.range_

    @range.setter
    def range(self, range_: tuple[float, float]):
        self.range_ = range_

    def is_in_range(self, value: float) -> bool:
        return not self.has_range or self.range[0] <= value <= self.range[1]

    def validate(self, value: str) -> bool:
        return _is_int(str(value)) and self.is_in_range(int(value))
