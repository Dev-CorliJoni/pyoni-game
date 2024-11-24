from dataclasses import dataclass


@dataclass(frozen=True)
class SpriteSheetLocator:
    x: int = None
    y: int = None
    width: int = None
    height: int = None

    def locator_tuple(self):
        return self.x, self.y, self.width, self.height

    def is_locator_empty(self):
        return self.x is None and self.y is None and self.width is None and self.height is None

    def is_locator_valid(self):
        return self.x is not None and self.y is not None and self.width is not None and self.height is not None
