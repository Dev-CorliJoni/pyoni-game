from dataclasses import dataclass

from pyonigame.models.components.image_data import SpriteSheetLocator


@dataclass(frozen=True)
class AnimationSpriteSheetLocator(SpriteSheetLocator):
    interval: float = 0.1
