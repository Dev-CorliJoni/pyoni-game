from enum import Enum


class ExpandableEnum(Enum):
    @classmethod
    def add(cls, name, value):
        new_member = object.__new__(cls)
        new_member._value_ = value
        new_member._name_ = name
        setattr(cls, name, new_member)
        cls._member_names_.append(name)
        cls._member_map_[name] = new_member
        cls._value2member_map_[value] = new_member
        return new_member
