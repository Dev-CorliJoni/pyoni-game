from pyonigame.helper import DirObject, DirObjectIO


class _TextResource(DirObject):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs, encapsulation=lambda v: _TextResource(v))

    def translate(self, language):
        for language in (language, "en"):
            if hasattr(self, language):
                return getattr(self, language)

        return None


class TextResource(_TextResource):
    def __init__(self, path):
        super().__init__(DirObjectIO(path).load())
