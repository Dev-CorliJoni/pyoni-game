import pygame


class SpriteSheetLoader:
    def __init__(self, path):
        self.sprite_sheet = pygame.image.load(path).convert_alpha()
        self.images = {}

    def get_sprite(self, x, y, width, height, scale_by=1, rotate_degrees=0, mirror_x=False, mirror_y=False):
        cache_key = (x, y, width, height, scale_by, rotate_degrees, mirror_x, mirror_y)
        # If already cached, return the stored image
        if cache_key in self.images:
            return self.images[cache_key]

        sprite = pygame.Surface((width, height), pygame.SRCALPHA)
        sprite.blit(self.sprite_sheet, (0, 0), pygame.Rect(x, y, width, height))

        # Apply transformations if requested
        if scale_by != 1:
            sprite = pygame.transform.scale_by(sprite, scale_by)
        if rotate_degrees != 0:
            sprite = pygame.transform.rotate(sprite, rotate_degrees)
        if mirror_x or mirror_y:
            sprite = pygame.transform.flip(sprite, mirror_x, mirror_y)

        # Cache the transformed image
        self.images[cache_key] = sprite

        return sprite
