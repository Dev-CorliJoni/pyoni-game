from pyonigame.components.controls.validators.regex_validator import _is_float
from pyonigame.components.controls.validators import IntValidator


class FloatValidator(IntValidator):

    def validate(self, value: str) -> bool:
        return _is_float(value) and self.is_in_range(float(value))
