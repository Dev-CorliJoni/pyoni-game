from pyonigame.events import RequestType
from pyonigame.models import DictObject


class Request:
    COUNTER = 0

    def __init__(self, type_: RequestType, data: DictObject):
        self.id = Request.COUNTER
        Request.COUNTER += 1

        self.type: RequestType = type_
        self.data: DictObject = data

    def request(self):
        vars_ = vars(self)
        obj_ = DictObject({key: vars_[key] for key in vars_ if key == key.lower()})
        obj_.type = self.type.value
        return obj_

    def __repr__(self):
        return (
            f"{self.__class__.__name__}("
            f"id={self.id}, "
            f"type={self.type!r}, "
            f"data={self.data!r})"
        )

    @staticmethod
    def text_shape_resolver():
        return Request(RequestType.TEXT_SHAPE_RESOLVER, DictObject())
