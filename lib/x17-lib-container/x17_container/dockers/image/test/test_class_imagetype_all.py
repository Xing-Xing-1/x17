import pytest
from x17_container.dockers.image.imagetype import ImageType

def test_image_type_enum_integrity():
    assert ImageType.PULL.value == "PULL"
    assert ImageType.BUILD.value == "BUILD"

    assert ImageType("PULL") == ImageType.PULL
    assert ImageType("BUILD") == ImageType.BUILD

    names = [e.name for e in ImageType]
    assert "PULL" in names
    assert "BUILD" in names