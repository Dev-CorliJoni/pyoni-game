from dataclasses import dataclass


@dataclass(frozen=True)
class AdditionalSpriteData:
    image_rotation: int = 0
    mirror_x: bool = False
    mirror_y: bool = False
