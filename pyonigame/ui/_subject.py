class Subject:
    def __init__(self, settings, *observers):
        self._observers = []
        for observer in observers:
            observer.apply_settings(settings)
            self._observers.append(observer)

    def get_inputs(self):
        for observer in self._observers:
            if observer.opened:
                for input_ in observer.get_inputs():
                    yield input_

        # Todo Maybe obsolete since EventManager could stop the event
        if all([observer.opened is False for observer in self._observers]):
            yield None

    def get_font_dimensions(self, text, font, size):
        # Todo Remove if request and request answer implemented
        for observer in self._observers:
            if observer.opened:
                return observer.get_font_dimension(text, font, size)

    def update(self, requests, updates):
        for observer in self._observers:
            if observer.opened:
                observer.update(requests, updates)
