import pygame
from pygame import locals
from pygame.locals import *

from pyonigame.helper import DirObject
from pyonigame.ui.pygame_ import SpriteSheetLoader, FontLoader


class PygameObserver:

    def __init__(self, settings):
        pygame.init()
        self._key_events = {getattr(locals, var): var for var in dir(locals) if
                            not var.startswith("__") and var.startswith("K_")}

        self.settings = settings
        self.mouse_functions = {BUTTON_LEFT: "left", BUTTON_MIDDLE: "middle", BUTTON_RIGHT: "right",
                                BUTTON_WHEELUP: "up", BUTTON_WHEELDOWN: "down"}
        self.sort_order = ("background", "game_element", "control")

        self.opened = False
        self.refresh = True
        self._clock = None
        self._screen = None
        self._background_image = None

        self.font_loader = FontLoader()

        self.sprite_sheet_loader = {}
        self._objects = {}

        self._apply_settings(settings)

    def _create_screen(self, dimension, vsync, *flags):
        flag = pygame.DOUBLEBUF | pygame.SRCALPHA
        for f in flags:
            flag |= f
        self._screen = pygame.display.set_mode(dimension, flag, vsync=vsync)

    def _apply_settings(self, settings):
        if settings.display.mode == "fullscreen":
            self._create_screen((0, 0), settings.display.vsync, pygame.FULLSCREEN)
            # change settings dimension
            dimension = self._screen.get_size()
            settings.display.dimension.width = dimension[0]
            settings.display.dimension.height = dimension[1]
        elif settings.display.mode == "dimension":
            dimension = settings.display.dimension
            # get the highest width and height of all attached screens
            display_sizes = pygame.display.get_desktop_sizes()
            max_width, max_height = max([size[0] for size in display_sizes]), max([size[1] for size in display_sizes])
            # check if the window is visible on the screen and if not don't reset the window
            if dimension.width > max_width or dimension.height > max_height:
                screen_info = pygame.display.Info()
                dimension.width, dimension.height = screen_info.current_w, screen_info.current_h

            self._create_screen((dimension.width, dimension.height), settings.display.vsync)

        pygame.display.set_caption(settings.caption)
        self._clock = pygame.time.Clock()

        self._screen.fill((255, 255, 255))
        pygame.display.flip()

        self.opened = True

    def get_inputs(self):
        clicked, click_released, scroll = ("",) * 3

        # event.type == pygame.MOUSEMOTION, Joystick-Events
        for event in pygame.event.get():
            if event.type == QUIT:
                self.quit()
            elif event.type == WINDOWFOCUSGAINED or event.type == WINDOWFOCUSLOST:
                yield DirObject({"type": "focus", "value": event.type == WINDOWFOCUSGAINED})
            elif event.type in (KEYDOWN, KEYUP) and event.key in self._key_events and "K_" in self._key_events[event.key]:
                value, unicode = self._key_events[event.key].replace("K_", "").lower(), event.unicode
                type_ = "key" if event.type == KEYDOWN else "key_end"

                #if not (event.mod & KMOD_SHIFT) and len(value) == 1:
                #    unicode = unicode.lower()
                yield DirObject({"type": type_, "value": f"{value}", "unicode": f"{unicode}"})

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in (BUTTON_WHEELUP, BUTTON_WHEELDOWN):
                    scroll = self.mouse_functions[event.button]
                else:
                    clicked = self.mouse_functions[event.button]

            elif event.type == pygame.MOUSEBUTTONUP and event.button not in (BUTTON_WHEELUP, BUTTON_WHEELDOWN):
                click_released = self.mouse_functions[event.button]

        if self.opened:
            mouse_pos = pygame.mouse.get_pos()
            for obj in filter(lambda o: o.type in ("rect", "sprite", "animation", "text"), self._objects.values()):

                rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                if rect.collidepoint(mouse_pos):
                    if clicked != "":
                        yield DirObject({"type": "click", "id": obj.id, "pos": mouse_pos, "button": clicked})
                    elif click_released != "":
                        yield DirObject({"type": "click_end", "id": obj.id, "pos": mouse_pos, "button": click_released})
                    if scroll != "":
                        yield DirObject({"type": "scroll", "id": obj.id, "pos": mouse_pos, "value": scroll})
                    yield DirObject({"type": "hover", "id": obj.id, "pos": mouse_pos})

    def update(self, updates: list[DirObject]):

        for obj in filter(lambda o: o.type == "command", updates):
            if obj.value == "quit":
                self.quit()
                return
            elif obj.value == "refresh":
                self.refresh = True
            elif obj.value == "refresh_settings":
                self._apply_settings(self.settings)

        width, height = self._screen.get_size()
        # only update visible objects
        filter_ = lambda o: (o.type != "command" and o.x + o.width >= 0 and o.y + o.height >= 0 and o.x <= width and o.y <= height and (o.state_changed or self.refresh or o.layer == "control"))

        for update_data in sorted(filter(filter_, updates), key=lambda u: self.sort_order.index(u.layer)):
            if update_data.type in ("sprite", "animation"):
                if update_data.path in self.sprite_sheet_loader:
                    sprite_sheet = self.sprite_sheet_loader[update_data.path]
                else:
                    sprite_sheet = self.sprite_sheet_loader[update_data.path] = SpriteSheetLoader(update_data.path)

                if update_data.type == "sprite":
                    coordinates = update_data.sprite_coordinates
                else:  # update_data.type == "animation"
                    coordinates = update_data.animation_coordinates[update_data.current_image]

                sprite = sprite_sheet.get_sprite(*coordinates, scale_by=update_data.image_scale, rotate_degrees=update_data.image_rotation,
                                                 mirror_x=update_data.image_mirrored_x, mirror_y=update_data.image_mirrored_y)
                update_data.update(obj=sprite)
            elif update_data.type == "text":
                font = self.font_loader.get_font(update_data.font, update_data.size)
                font.set_bold(update_data.bold)
                update_data.obj = font.render(update_data.text, True, update_data.color)

            elif update_data.type in ("circle", "rect", "line"):
                if update_data.color != "transparent":
                    {
                        "line": self.update_line,
                        "rect": self.update_rect,
                        "circle": self.update_circle,
                    }[update_data.type](update_data)

            if update_data.type in ("text", "sprite", "animation"):
                self._screen.blit(update_data.obj, (update_data.x, update_data.y))

            self._objects[update_data.id] = update_data

        self.refresh = False
        pygame.display.flip()
        if self.settings.display.vsync:
            self._clock.tick()
        else:
            self._clock.tick(self.settings.display.fps)

    def update_line(self, update_data):
        pos1, pos2 = update_data.pos1, update_data.pos2
        pygame.draw.line(self._screen, update_data.color, pos1, pos2, update_data.size)

    def update_circle(self, update_data):
        pygame.draw.circle(self._screen, update_data.color, (update_data.x, update_data.y), update_data.radius)

    def update_rect(self, update_data):
        rect = pygame.Rect(update_data.x, update_data.y, update_data.width, update_data.height)

        if update_data.border_color != "transparent":
            pygame.draw.rect(self._screen, update_data.border_color,
                             rect.inflate(update_data.border_width * 2, update_data.border_width * 2),
                             border_radius=update_data.border_radius)
        pygame.draw.rect(self._screen, update_data.color, rect, border_radius=update_data.border_radius)

    def quit(self):
        pygame.quit()
        self.opened = False

    def get_font_dimension(self, text, font, size):
        return self.font_loader.get_font(font, size).size(text)
