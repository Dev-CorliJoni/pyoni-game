from importlib.resources import files


def get_resource_path(name):
    return files('pyonigame.resources') / name
