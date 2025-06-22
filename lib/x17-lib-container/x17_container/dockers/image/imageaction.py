from enum import Enum


class ImageActionMode(str, Enum):
    PULL = "PULL"  # Pull image from registry only
    BUILD = "BUILD"  # Build image from Dockerfile only
    MANUAL = "MANUAL"  # Manual mode, no actions taken


class ImageAction:

    @classmethod
    def from_str(cls, mode_str: str) -> "ImageAction":
        try:
            mode = ImageActionMode(mode_str)
        except ValueError:
            mode = ImageActionMode.MANUAL
        return cls(mode=mode)

    def __init__(
        self,
        mode: ImageActionMode = ImageActionMode.MANUAL,
    ):
        self.mode = ImageActionMode(mode)

    @property
    def dict(self) -> dict:
        return {"mode": self.mode.value}

    def __str__(self):
        return self.mode.value

    def __repr__(self):
        return f"{self.__class__.__name__}(mode={self.mode.value})"

    @property
    def is_manual(self) -> bool:
        return self.mode == ImageActionMode.MANUAL

    @property
    def is_pull(self) -> bool:
        return self.mode == ImageActionMode.PULL

    @property
    def is_build(self) -> bool:
        return self.mode == ImageActionMode.BUILD

    def __eq__(self, other):
        if isinstance(other, ImageAction):
            return self.mode == other.mode
        elif isinstance(other, str):
            return self.mode == ImageActionMode(other)
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

