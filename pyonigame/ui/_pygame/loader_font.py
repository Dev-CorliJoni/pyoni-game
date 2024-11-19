import pygame


class FontLoader:

    def __init__(self):
        self.fonts = {
            "arial": "Arial",
        }

        self.loaded_fonts = {}

    def add_font(self, name, font):
        self.fonts[name] = font

    def get_font(self, name, size):
        font_reference = self.fonts[name] if name in self.fonts else None

        if (name, size) not in self.loaded_fonts:
            if "." in font_reference:
                font = pygame.font.Font(font_reference, size)
            else:
                font = pygame.font.SysFont(font_reference, size)

            self.loaded_fonts[(name, size)] = font

        return self.loaded_fonts[(name, size)]
