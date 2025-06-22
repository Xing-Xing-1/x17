from enum import Enum

class ImageType(str, Enum):
    PULL = "PULL"  # Remote image, typically pulled from a registry
    BUILD = "BUILD"  # Build image, created from a Dockerfile
    MANUAL = "MANUAL"  # Manual image, no specific action defined