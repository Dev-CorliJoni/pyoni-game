from __future__ import annotations


def _convert_field(value):
    if isinstance(value, DictObject):
        return value.to_dict()
    elif isinstance(value, list):
        return [_convert_field(item) for item in value]
    return value


def _override_list(self_list, list_):
    for item in list_:
        if isinstance(item, DictObject) and item not in self_list:
            self_list.append(item.copy())
        elif isinstance(item, list) and item not in self_list:
            self_list.append(_override_list([], item))
        elif item not in self_list:
            self_list.append(item)
    return self_list


def _format_dict_obj(obj, level):
    """Helper method for pretty string representation."""
    indent = "  " * level
    if isinstance(obj, DictObject):
        items = ",\n".join(
            f"{indent}  {repr(key)}: {_format_dict_obj(value, level + 1)}"
            for key, value in obj.items()
        )
        return f"{{\n{items}\n{indent}}}"
    elif isinstance(obj, list):
        items = ",\n".join(f"{indent}  {_format_dict_obj(value, level + 1)}" for value in obj)
        return f"[\n{items}\n{indent}]"
    else:
        return repr(obj)


class DictObject(dict):
    def __init__(self, *args, encapsulation=lambda v: DictObject(v), **kwargs):
        super(DictObject, self).__init__(*args, **kwargs)

        for key, value in self.items():
            if type(value) is dict:
                self[key] = encapsulation(value)

    def __repr__(self) -> str:
        class_name = self.__class__.__name__
        content = super().__repr__()
        return f"{class_name}({content})"

    def __str__(self) -> str:
        return _format_dict_obj(self, level=0)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(f"'DictObject' object has no attribute '{key}'")

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError:
            raise AttributeError(f"'DictObject' object has no attribute '{key}'")

    def copy(self) -> DictObject:
        copied_data = {}
        for key, value in self.items():
            if isinstance(value, DictObject):
                # Recursively copy nested DictObject
                copied_data[key] = value.copy()
            elif isinstance(value, list):
                # Recursively copy lists, ensuring nested items are copied
                copied_data[key] = [
                    item.copy() if isinstance(item, DictObject) else item for item in value
                ]
            elif isinstance(value, dict):
                # Copy nested dictionaries as regular dicts
                copied_data[key] = value.copy()
            else:
                # For other objects, use their `copy` method if available or copy as is
                copied_data[key] = value.copy() if hasattr(value, 'copy') else value

        # Reinitialize using the copied data
        return self.__class__(**copied_data)

    def override(self, dict_object: DictObject) -> None:
        for key, value in dict_object.items():
            if isinstance(value, DictObject):
                if not hasattr(self, key):
                    setattr(self, key, value.__class__())
                getattr(self, key).override(value)
            elif isinstance(value, list):
                self_list = getattr(self, key) if hasattr(self, key) else []
                setattr(self, key, _override_list(self_list, value))
            else:
                setattr(self, key, value)

    def to_dict(self) -> dict:
        return {key: _convert_field(value) for key, value in self.items()}
