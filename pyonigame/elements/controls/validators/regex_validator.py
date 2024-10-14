import re


def _validate(regex: str, value: str) -> bool:
    return bool(re.match(regex, value))


def _is_int(value: str) -> bool:
    return _validate(r'^-?\d+$', value)


def _is_float(value: str) -> bool:
    return _validate(r'^-?\d+(\.\d+)?$', value)


class RegexValidator:

    def __init__(self, regex: str):
        self.regex = regex

    def validate(self, value: str) -> bool:
        return _validate(self.regex, value)
