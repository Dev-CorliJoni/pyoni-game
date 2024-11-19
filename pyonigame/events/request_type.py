from enum import Enum


class RequestType(Enum):
    QUIT = "quit"
    REFRESH = "refresh"
    REFRESH_SETTINGS = "refresh_settings"
    TEXT_SHAPE_RESOLVER = "text_shape_resolver"
