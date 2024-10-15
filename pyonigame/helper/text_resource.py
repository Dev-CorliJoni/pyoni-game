from pyonigame.helper import DictObject, IODictObject


class _TextResource(DictObject):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, encapsulation=lambda v: _TextResource(v))

    def translate(self, language):
        for language in (language, "en"):
            if hasattr(self, language):
                return getattr(self, language)

        return None


class TextResource(_TextResource):
    def __init__(self, path):
        super().__init__(IODictObject(path).load())


def deliver_text_resource(path):
    def decorator(func):
        def wrapper(*args, **kwargs):
            resource = TextResource(path)
            return func(resource, *args, **kwargs)

        return wrapper
    return decorator
