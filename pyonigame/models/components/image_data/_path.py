from dataclasses import dataclass


@dataclass(frozen=True)
class _Path:
    image_path: str
