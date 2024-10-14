class Subject(object):

    def __init__(self, *observers):
        self._observers = []
        self._observers.extend(observers)

    def get_inputs(self):
        for observer in self._observers:
            if observer.opened:
                for input_ in observer.get_inputs():
                    yield input_

        if all([observer.opened is False for observer in self._observers]):
            yield None

    def get_font_dimensions(self, text, font, size):
        for observer in self._observers:
            if observer.opened:
                return observer.get_font_dimension(text, font, size)

    def update(self, updates):
        for observer in self._observers:
            if observer.opened:
                observer.update(updates)
