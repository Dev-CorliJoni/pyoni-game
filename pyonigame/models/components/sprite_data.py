from dataclasses import dataclass


@dataclass(frozen=True)
class _Path:
    image_path: str


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


@dataclass(frozen=True)
class SpriteData(SpriteSheetLocator, _Path):
    image_rotation: int = 0
    mirror_x: bool = False
    mirror_y: bool = False

    @staticmethod
    def get_sprite_group_data(path: str, locators: list[list[SpriteSheetLocator]], image_rotation: int = 0, mirror_x: bool = False, mirror_y: bool = False):
        result = []
        for y_axis in locators:
            inner_result = []
            result.append(inner_result)
            for loc in y_axis:
                inner_result.append(SpriteData(path, loc.x, loc.y, loc.width, loc.height, image_rotation, mirror_x, mirror_y))
        return result


