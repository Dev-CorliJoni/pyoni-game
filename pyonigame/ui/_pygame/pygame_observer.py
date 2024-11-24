from typing import Generator

import pygame
from pygame import locals
from pygame.locals import *

from pyonigame.models.settings import DisplayMode
from pyonigame.events import Request
from pyonigame.models import DictObject
from pyonigame.helper._resource_path_provider import get_resource_path
from pyonigame.ui._pygame import SpriteSheetLoader, FontLoader
from pyonigame.templates import UIObserver


class PygameObserver(UIObserver):

    def __init__(self) -> None:
        super().__init__()
        pygame.init()
        self._key_events = {getattr(locals, var): var for var in dir(locals) if
                            not var.startswith("__") and var.startswith("K_")}

        self._mouse_functions = {BUTTON_LEFT: "left", BUTTON_MIDDLE: "middle", BUTTON_RIGHT: "right",
                                 BUTTON_WHEELUP: "up", BUTTON_WHEELDOWN: "down"}
        self._sort_order = ("background", "game_element", "control")

        self._fps: int = 60
        self._vsync: bool = False
        self._refresh: bool = True
        self._provide_text_shape_resolver: bool = False

        self._screen_changed = None

        self._clock = None
        self._screen = None
        self._background_image = None

        self._font_loader = FontLoader()

        self._sprite_sheet_loader = {}
        self._objects = {}

    def _create_screen(self, dimension, vsync, *flags):
        flag = pygame.DOUBLEBUF | pygame.SRCALPHA
        for f in flags:
            flag |= f
        self._screen = pygame.display.set_mode(dimension, flag, vsync=vsync)

    def apply_settings(self, settings: DictObject) -> None:
        self._fps = settings.fps
        self._vsync = settings.vsync

        for font in settings.custom_fonts:
            self._font_loader.add_font(font.name, font.font_path)

        if self._screen is not None:
            screen_info = pygame.display.Info()
            old_width, old_height = screen_info.current_w, screen_info.current_h
        else:
            old_width, old_height = 0, 0

        new_width, new_height = settings.dimension.width, settings.dimension.height

        if settings.mode == DisplayMode.FULLSCREEN:
            self._create_screen((0, 0), self._vsync, pygame.FULLSCREEN)
            # change settings dimension
            dimension = self._screen.get_size()
            new_width = dimension[0]
            new_height = dimension[1]
        elif settings.mode == DisplayMode.DIMENSION:
            # get the highest width and height of all attached screens
            display_sizes = pygame.display.get_desktop_sizes()
            max_width, max_height = max([size[0] for size in display_sizes]), max([size[1] for size in display_sizes])
            # check if the window is visible on the screen and if not don't reset the window
            if new_width > max_width or new_height > max_height:
                new_width, new_height = old_width, old_height

            self._create_screen((new_width, new_height), self._vsync)

        if old_width != new_width or old_height != new_height:
            self._screen_changed = {"width": new_width, "height": new_height}

        if hasattr(settings, "icon"):
            icon_path = settings.icon
        else:
            icon_path = get_resource_path("images/icon.png")

        icon_image = pygame.image.load(icon_path)
        pygame.display.set_icon(icon_image)

        pygame.display.set_caption(settings.caption)
        self._clock = pygame.time.Clock()
        self.opened = True

    def get_inputs(self) -> Generator[DictObject, None, None]:
        clicked, click_released, scroll = ("",) * 3
        events = pygame.event.get()

        if self._provide_text_shape_resolver:
            self._provide_text_shape_resolver = False
            yield DictObject({"type": "request_answer", "answer_type": "text_shape_resolver", "value": self.get_font_dimension})

        if self._screen_changed is not None:
            yield DictObject({"type": "screen_size", **self._screen_changed})
            self._screen_changed = None

        # event.type == pygame.MOUSEMOTION
        for event in events:
            if event.type == QUIT:
                yield DictObject({"type": "quit"})
            elif event.type == WINDOWFOCUSGAINED or event.type == WINDOWFOCUSLOST:
                yield DictObject({"type": "window_focus_changed", "value": event.type == WINDOWFOCUSGAINED})
            elif event.type in (KEYDOWN, KEYUP) and event.key in self._key_events and "K_" in self._key_events[event.key]:
                value, unicode = self._key_events[event.key].replace("K_", "").lower(), event.unicode
                type_ = "key" if event.type == KEYDOWN else "key_end"
                yield DictObject({"type": type_, "value": f"{value}", "unicode": f"{unicode}"})

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button in (BUTTON_WHEELUP, BUTTON_WHEELDOWN):
                    scroll = self._mouse_functions[event.button]
                else:
                    clicked = self._mouse_functions[event.button]

            elif event.type == pygame.MOUSEBUTTONUP and event.button not in (BUTTON_WHEELUP, BUTTON_WHEELDOWN):
                click_released = self._mouse_functions[event.button]

        if self.opened:
            mouse_pos = pygame.mouse.get_pos()
            for obj in filter(lambda o: o.type in ("rect", "sprite", "animation", "text"), self._objects.values()):

                rect = pygame.Rect(obj.x, obj.y, obj.width, obj.height)
                if rect.collidepoint(mouse_pos):
                    if clicked != "":
                        yield DictObject({"type": "click", "id": obj.id, "pos": mouse_pos, "value": clicked})
                    elif click_released != "":
                        yield DictObject({"type": "click_end", "id": obj.id, "pos": mouse_pos, "value": click_released})
                    if scroll != "":
                        yield DictObject({"type": "scroll", "id": obj.id, "pos": mouse_pos, "value": scroll})
                    yield DictObject({"type": "hover", "id": obj.id, "pos": mouse_pos})

    def _filter_updates(self, o):
        screen_width, screen_height = self._screen.get_size()
        # only update visible objects

        show_object = o.state_changed or self._refresh or o.layer == "control"

        if o.type == "line":
            x, y = min(o.pos1[0], o.pos2[0]) - o.size, min(o.pos1[1], o.pos2[1]) - o.size
            width, height = max(o.pos1[0], o.pos2[0]) - x + o.size * 2, max(o.pos1[1], o.pos2[1]) - y + o.size * 2
        elif o.type == "circle":
            x, y = o.x - o.radius, o.y - o.radius
            width, height = o.radius * 2, o.radius * 2
        else:
            x, y, width, height = o.x, o.y, o.width, o.height

        return show_object and x + width >= 0 and y + height >= 0 and x <= screen_width and y <= screen_height

    def update(self, requests: list[Request], updates: list[DictObject]) -> None:
        for obj in requests:
            if obj.type == "quit":
                return self._quit()
            elif obj.type == "refresh":
                self._refresh = True
            elif obj.type == "refresh_settings":
                self.apply_settings(obj.data)
            elif obj.type == "text_shape_resolver":
                self._provide_text_shape_resolver = True

        if self._refresh:
            self._screen.fill((255, 255, 255))

        for update_data in sorted(filter(self._filter_updates, updates), key=lambda u: self._sort_order.index(u.layer)):
            if update_data.type in ("sprite", "animation"):
                if update_data.path in self._sprite_sheet_loader:
                    sprite_sheet = self._sprite_sheet_loader[update_data.path]
                else:
                    sprite_sheet = self._sprite_sheet_loader[update_data.path] = SpriteSheetLoader(update_data.path)

                coordinates = update_data.sprite_coordinates
                sprite = sprite_sheet.get_sprite(*coordinates, scale_by=update_data.image_scale, rotate_degrees=update_data.image_rotation,
                                                 mirror_x=update_data.image_mirrored_x, mirror_y=update_data.image_mirrored_y)
                update_data.update(obj=sprite)
            elif update_data.type == "text":
                font = self._font_loader.get_font(update_data.font, update_data.size)
                font.set_bold(update_data.bold)
                update_data.obj = font.render(update_data.text, True, update_data.color)

            elif update_data.type in ("circle", "rect", "line"):
                if update_data.color != "transparent":
                    {
                        "line": self._update_line,
                        "rect": self._update_rect,
                        "circle": self._update_circle,
                    }[update_data.type](update_data)

            if update_data.type in ("text", "sprite", "animation"):
                self._screen.blit(update_data.obj, (update_data.x, update_data.y))

            self._objects[update_data.id] = update_data

        self._refresh = False
        pygame.display.flip()
        if self._vsync:
            self._clock.tick()
        else:
            self._clock.tick(self._fps)

    def _update_line(self, update_data):
        pos1, pos2 = update_data.pos1, update_data.pos2
        pygame.draw.line(self._screen, update_data.color, pos1, pos2, update_data.size)

    def _update_circle(self, update_data):
        pygame.draw.circle(self._screen, update_data.color, (update_data.x, update_data.y), update_data.radius)

    def _update_rect(self, update_data):
        rect = pygame.Rect(update_data.x, update_data.y, update_data.width, update_data.height)

        if update_data.border_color != "transparent":
            pygame.draw.rect(self._screen, update_data.border_color,
                             rect.inflate(update_data.border_width * 2, update_data.border_width * 2),
                             border_radius=update_data.border_radius)
        pygame.draw.rect(self._screen, update_data.color, rect, border_radius=update_data.border_radius)

    def _quit(self):
        pygame.quit()
        self.opened = False

    def get_font_dimension(self, text, font, size):
        return self._font_loader.get_font(font, size).size(text)
