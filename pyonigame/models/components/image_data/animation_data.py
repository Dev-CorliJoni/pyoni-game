from __future__ import annotations
from dataclasses import dataclass

from pyonigame.models.components.image_data import AnimationSpriteSheetLocator, SpriteSheetLocator
from pyonigame.models.components.image_data._animation_sprite_data import AnimationSpriteData


@dataclass(frozen=True)
class AnimationData(list[AnimationSpriteData]):

    @staticmethod
    def get_animation_data(path: str, locators: list[AnimationSpriteSheetLocator], image_rotation: int = 0, mirror_x: bool = False, mirror_y: bool = False) -> AnimationData:
        data = AnimationData()
        data.extend(AnimationSpriteData.gen_animation_sprite_data(path, *locators, image_rotation=image_rotation, mirror_x=mirror_x, mirror_y=mirror_y))
        return data

    @staticmethod
    def get_static_interval_animation_data(path: str, locators: list[SpriteSheetLocator], interval: float = 0.1, image_rotation: int = 0, mirror_x: bool = False, mirror_y: bool = False) -> AnimationData:
        data = AnimationData()
        locators = [AnimationSpriteSheetLocator(loc.x, loc.y, loc.width, loc.height, interval) for loc in locators]
        data.extend(AnimationSpriteData.gen_animation_sprite_data(path, *locators, image_rotation=image_rotation, mirror_x=mirror_x, mirror_y=mirror_y))
        return data
