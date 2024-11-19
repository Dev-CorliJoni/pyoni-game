from pyonigame.models import DictObject
from pyonigame.models.settings import Language
from pyonigame.helper import IODictObject


class _TextResource(DictObject):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, encapsulation=lambda v: _TextResource(v))

    def translate(self, language: Language):
        for language in (language.value, "en"):
            if hasattr(self, language):
                return getattr(self, language)

        return None


class TextResource(_TextResource):
    def __init__(self, path: str):
        super().__init__(IODictObject(path).load())


def deliver_text_resource(path: str):
    def decorator(func):
        def wrapper(*args, **kwargs):
            resource = TextResource(path)
            return func(resource, *args, **kwargs)

        return wrapper
    return decorator
