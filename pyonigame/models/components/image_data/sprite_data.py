from __future__ import annotations
from dataclasses import dataclass

from pyonigame.models.components.image_data import SpriteSheetLocator
from pyonigame.models.components.image_data._additional_sprite_data import AdditionalSpriteData
from pyonigame.models.components.image_data._path import _Path


@dataclass(frozen=True)
class SpriteData(AdditionalSpriteData, SpriteSheetLocator, _Path):

    @staticmethod
    def get_sprite_group_data(path: str, locators: list[list[SpriteSheetLocator]], image_rotation: int = 0, mirror_x: bool = False, mirror_y: bool = False) -> list[list[SpriteData]]:
        result = []
        for y_axis in locators:
            inner_result = []
            result.append(inner_result)
            for loc in y_axis:
                inner_result.append(SpriteData(path, loc.x, loc.y, loc.width, loc.height, image_rotation, mirror_x, mirror_y))
        return result
