import pytest
from x17_container.dockers.image.imagetype import ImageType

def test_image_type_enum_integrity():
    assert ImageType.HYBRID.value == "HYBRID"
    assert ImageType.SINGLETON.value == "SINGLETON"
    assert ImageType.CUSTOM.value == "CUSTOM"
    assert ImageType.UNKNOWN.value == "UNKNOWN"
    assert ImageType.LOADED.value == "LOADED"

    assert ImageType("HYBRID") == ImageType.HYBRID
    assert ImageType("LOADED") == ImageType.LOADED

    names = [e.name for e in ImageType]
    assert "HYBRID" in names
    assert "SINGLETON" in names
    assert "CUSTOM" in names
    assert "UNKNOWN" in names
    assert "LOADED" in names