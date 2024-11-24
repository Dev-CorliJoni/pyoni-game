from dataclasses import dataclass

from pyonigame.models.components.image_data import AnimationSpriteSheetLocator
from pyonigame.models.components.image_data._additional_sprite_data import AdditionalSpriteData
from pyonigame.models.components.image_data._path import _Path


@dataclass(frozen=True)
class AnimationSpriteData(AdditionalSpriteData, AnimationSpriteSheetLocator, _Path):

    @staticmethod
    def gen_animation_sprite_data(path: str, *locators: AnimationSpriteSheetLocator, image_rotation: int = 0, mirror_x: bool = False, mirror_y: bool = False):
        for loc in locators:
            yield AnimationSpriteData(path, loc.x, loc.y, loc.width, loc.height, loc.interval, image_rotation, mirror_x, mirror_y)
