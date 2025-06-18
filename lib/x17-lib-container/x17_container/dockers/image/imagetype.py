from enum import Enum

class ImageType(str, Enum):
    HYBRID = "HYBRID"  # Hybrid image, can be used for both container and build
    SINGLETON = "SINGLETON"  # Singleton image, used for a single container instance
    CUSTOM = "CUSTOM"  # Custom image, user-defined with specific parameters
    UNKNOWN = "UNKNOWN"  # Unknown image type, not specified or recognized
    LOADED = "LOADED"  # Image loaded from a docker file image object in python runtime