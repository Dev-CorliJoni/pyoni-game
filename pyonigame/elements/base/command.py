from pyonigame.elements.base import Base


class Command(Base):

    QUIT = "quit"
    REFRESH = "refresh"
    REFRESH_SETTINGS = "refresh_settings"

    def __init__(self, command):
        super().__init__("command", "")
        self.value = command
