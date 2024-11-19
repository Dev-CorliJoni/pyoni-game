from enum import Enum
from typing import Any, Type

from pyonigame.models import DictObject


def from_dict_obj(dict_object: DictObject, attr_name: str, default: Any) -> Any:
    try:
        return getattr(dict_object, attr_name)
    except AttributeError:
        return default


def enum_from_dict_obj(dict_object: DictObject, attr_name: str, enum_type: Type[Enum], default: Enum) -> Enum:
    try:
        return enum_type(from_dict_obj(dict_object, attr_name, default))
    except ValueError:
        return default


def list_from_dict_obj(dict_object: DictObject, attr_name: str, default: list) -> list:
    list_obj = from_dict_obj(dict_object, attr_name, default)
    if type(list_obj) is DictObject:
        list_obj = [DictObject({key: value}) for key, value in list_obj.items()]
    if type(list_obj) is list:
        return list_obj
    return default
