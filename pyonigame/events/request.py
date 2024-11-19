from pyonigame.helper import DictObject


class Command:
    COUNTER = 0

    QUIT = "quit"
    REFRESH = "refresh"
    REFRESH_SETTINGS = "refresh_settings"

    def __init__(self, command, data):
        self.id = Command.COUNTER
        Command.COUNTER += 1

        self.command = command
        self.data = data

    def request(self):
        vars_ = vars(self)
        return DictObject({key: vars_[key] for key in vars_ if key == key.lower()})

