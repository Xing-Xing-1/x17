from x17_container.dockers.image.image import Image
from x17_container.dockers.image.imageaction import ImageAction
from x17_container.dockers.image.imageaction import ActionMode
import pytest

def test_action_mode_plan_behavior():
    assert ImageAction(ActionMode.PULL).plan() == {"pull": True, "build": False}
    assert ImageAction(ActionMode.BUILD).plan() == {"pull": False, "build": True}
    assert ImageAction(ActionMode.PULL_BUILD).plan() == {"pull": True, "build": True}
    assert ImageAction(ActionMode.AUTOMATIC).plan() == {"pull": True, "build": True}
    assert ImageAction(ActionMode.MANUAL).plan() == {"pull": False, "build": False}

def test_manual_and_automatic_flags():
    assert ImageAction(ActionMode.MANUAL).is_manual is True
    assert ImageAction(ActionMode.AUTOMATIC).is_automatic is True
    assert ImageAction(ActionMode.BUILD).is_manual is False
    assert ImageAction(ActionMode.BUILD).is_automatic is False

def test_from_str_valid_and_invalid():
    assert isinstance(ImageAction.from_str("PULL"), ImageAction)
    assert ImageAction.from_str("BUILD").plan() == {"pull": False, "build": True}
    assert ImageAction.from_str("INVALID") == ImageAction(ActionMode.AUTOMATIC)

def test_string_and_repr_outputs():
    action = ImageAction(ActionMode.BUILD)
    assert str(action) == "BUILD"
    assert "ImageAction" in repr(action)
    assert "BUILD" in repr(action)
    
