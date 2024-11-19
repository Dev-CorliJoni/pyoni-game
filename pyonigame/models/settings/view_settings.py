from __future__ import annotations
from typing import Optional

from pyonigame.models import DictObject
from pyonigame.models.settings import CustomFont, DisplayDimension, DisplayMode
from pyonigame.models.settings.helper import from_dict_obj, enum_from_dict_obj, list_from_dict_obj


class ViewSettings(DictObject):
    def __init__(self, caption: str, mode: DisplayMode, dimension: Optional[DisplayDimension] = None, vsync: bool = True, fps: int = 60, custom_fonts: Optional[list[CustomFont]] = None):
        dimension = dimension or DisplayDimension(800, 600)
        custom_fonts = custom_fonts or []
        super().__init__(caption=caption, mode=mode, dimension=dimension, fps=fps, vsync=vsync, custom_fonts=custom_fonts)

    @property
    def caption(self) -> str:
        return super().caption

    @caption.setter
    def caption(self, caption: str) -> None:
        super().caption = caption

    @property
    def mode(self) -> DisplayMode:
        return super().mode

    @mode.setter
    def mode(self, mode: DisplayMode) -> None:
        super().mode = mode

    @property
    def dimension(self) -> DisplayDimension:
        return super().dimension

    @dimension.setter
    def dimension(self, dimension: DisplayDimension) -> None:
        super().dimension = dimension

    @property
    def vsync(self) -> bool:
        return super().vsync

    @vsync.setter
    def vsync(self, vsync: bool) -> None:
        super().vsync = vsync

    @property
    def fps(self) -> int:
        return super().fps

    @fps.setter
    def fps(self, fps: int) -> None:
        super().fps = fps

    @property
    def custom_fonts(self) -> list[CustomFont]:
        return super().custom_fonts

    @custom_fonts.setter
    def custom_fonts(self, custom_fonts: list[CustomFont]) -> None:
        super().custom_fonts = custom_fonts

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["mode"] = data["mode"].value
        return data

    @staticmethod
    def from_dict_object(dict_object: DictObject) -> ViewSettings:
        caption = from_dict_obj(dict_object, "caption", "Game name")
        mode = DisplayMode(enum_from_dict_obj(dict_object, "mode", DisplayMode, DisplayMode.DIMENSION))
        dimension = from_dict_obj(dict_object, "dimension", DisplayDimension(800, 600))
        vsync = from_dict_obj(dict_object, "vsync", True)
        fps = from_dict_obj(dict_object, "fps", 60)
        custom_fonts = list_from_dict_obj(dict_object, "custom_fonts", [])
        custom_fonts = [CustomFont.from_dict_object(custom_font) for custom_font in custom_fonts]

        if mode == DisplayMode.DIMENSION and type(dimension) is not DisplayDimension:
            dimension = DisplayDimension.from_dict_object(dimension)

        return ViewSettings(caption, mode, dimension, vsync, fps, custom_fonts)
