class DirObject(dict):
    def __init__(self, *args, encapsulation=lambda v: DirObject(v), **kwargs):
        super(DirObject, self).__init__(*args, **kwargs)

        for key, value in self.items():
            if isinstance(value, dict):
                self[key] = encapsulation(value)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(f"'DirObject' object has no attribute '{key}'")

    def __setattr__(self, key, value):
        self[key] = value

    def __delattr__(self, key):
        try:
            del self[key]
        except KeyError:
            raise AttributeError(f"'DirObject' object has no attribute '{key}'")

    def copy(self):
        return DirObject(super().copy())

    def override(self, dir_object):
        def adopt_list(self_list, list_):
            for item in list_:
                if isinstance(item, DirObject):
                    self_list.append(DirObject())
                    self_list[-1].override(item)
                if isinstance(item, list):
                    self_list.append(adopt_list([], item))
                else:
                    self_list.append(item)
            return self_list

        for key, value in dir_object.items():
            if isinstance(value, DirObject):
                if not hasattr(self, key):
                    setattr(self, key, DirObject())
                getattr(self, key).override(value)
            elif isinstance(value, list):
                setattr(self, key, adopt_list([], value))
            else:
                setattr(self, key, value)

    def to_dict(self):
        result = {}
        for key, value in self.items():
            if isinstance(value, DirObject):
                result[key] = value.to_dict()
            else:
                result[key] = value
        return result
