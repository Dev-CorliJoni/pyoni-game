from __future__ import annotations
from typing import Optional

from pyonigame.models import DictObject
from pyonigame.models.settings import Language, Theme
from pyonigame.models.settings.helper import enum_from_dict_obj, from_dict_obj


class GameSettings(DictObject):
    def __init__(self, language: Language = Language.ENGLISH, theme: Theme = Theme.LIGHT, key_mapping: Optional[DictObject] = None, custom_settings: Optional[DictObject] = None):
        key_mapping = key_mapping or DictObject()
        custom_settings = custom_settings or DictObject()
        super().__init__(language=language, theme=theme, key_mapping=key_mapping, custom_settings=custom_settings)

    @property
    def language(self) -> Language:
        return super().language

    @language.setter
    def language(self, language: Language) -> None:
        super().language = language

    @property
    def theme(self) -> Theme:
        return super().theme

    @theme.setter
    def theme(self, theme: Theme) -> None:
        super().theme = theme

    @property
    def key_mapping(self) -> DictObject:
        return super().key_mapping

    @key_mapping.setter
    def key_mapping(self, key_mapping: DictObject) -> None:
        super().key_mapping = key_mapping

    @property
    def custom_settings(self) -> DictObject:
        return super().custom_settings

    @custom_settings.setter
    def custom_settings(self, custom_settings: DictObject) -> None:
        super().custom_settings = custom_settings

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["language"] = data["language"].value
        data["theme"] = data["theme"].value
        return data

    @staticmethod
    def from_dict_object(dict_object: DictObject) -> GameSettings:
        language = Language(enum_from_dict_obj(dict_object, "language", Language, Language.ENGLISH))
        theme = Theme(enum_from_dict_obj(dict_object, "theme", Theme, Theme.LIGHT))
        key_mapping = from_dict_obj(dict_object, "key_mapping", DictObject())
        custom_settings = from_dict_obj(dict_object, "custom_settings", DictObject())

        return GameSettings(language, theme, key_mapping, custom_settings)
