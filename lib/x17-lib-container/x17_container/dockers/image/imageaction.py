from enum import Enum
import warnings

class ActionMode(str, Enum):
    PULL = "PULL"               # Pull image from registry only
    PULL_BUILD = "PULL_BUILD"   # Pull image and build 
    BUILD = "BUILD"             # Build image from Dockerfile only
    AUTOMATIC = "AUTOMATIC"     # Automatic mode, pull and build if necessary
    MANUAL = "MANUAL"           # Manual mode, no actions taken


class ImageAction:
    
    @classmethod
    def from_str(cls, mode_str: str) -> "ImageAction":
        try:
            mode = ActionMode(mode_str)
        except ValueError:
            mode = ActionMode.AUTOMATIC
        return cls(mode=mode)
    
    def __init__(
        self,
        mode: ActionMode = ActionMode.AUTOMATIC,
    ):
        self.mode = ActionMode(mode)
    
    @property
    def dict(self) -> dict:
        return {
            "mode": self.mode.value,
        }
    
    def __str__(self):
        return self.mode.value
    
    def __repr__(self):
        attributes = []
        for unit, value in self.dict.items():
            attributes.append(f"{unit}={value}")
        return f"{self.__class__.__name__}({', '.join(attributes)})"
        
    @property
    def to_pull(self) -> bool:
        return self.mode in (ActionMode.PULL, ActionMode.PULL_BUILD, ActionMode.AUTOMATIC)
    
    @property
    def to_build(self) -> bool:
        return self.mode in (ActionMode.BUILD, ActionMode.PULL_BUILD, ActionMode.AUTOMATIC)
    
    @property
    def is_manual(self) -> bool:
        return self.mode == ActionMode.MANUAL
    
    @property
    def is_automatic(self) -> bool:
        return self.mode == ActionMode.AUTOMATIC
    
    @property
    def is_pull(self) -> bool:
        return self.mode == ActionMode.PULL
    
    @property
    def is_build(self) -> bool:
        return self.mode == ActionMode.BUILD
    
    @property
    def is_pull_and_build(self) -> bool:
        return self.mode == ActionMode.PULL_BUILD

    def plan(self) -> dict:
        return {
            "pull": self.to_pull,
            "build": self.to_build,
        }

    def __eq__(self, other):
        if isinstance(other, ImageAction):
            return self.mode == other.mode
        elif isinstance(other, str):
            return self.mode == ActionMode(other)
        return False
    
    def __ne__(self, other):
        return not self.__eq__(other)
    