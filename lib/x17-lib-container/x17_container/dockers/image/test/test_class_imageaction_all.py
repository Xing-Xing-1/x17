from x17_container.dockers.image.image import Image
from x17_container.dockers.image.imageaction import ImageAction
from x17_container.dockers.image.imageaction import ImageActionMode
import pytest

def test_action_mode_plan_behavior():
    build_action = ImageAction(ImageActionMode.BUILD)
    pull_action = ImageAction(ImageActionMode.PULL)
    manual_action = ImageAction(ImageActionMode.MANUAL)
    
    assert pull_action.is_manual is False
    assert pull_action.is_pull is True
    assert pull_action.is_build is False
    assert build_action.is_manual is False
    assert build_action.is_pull is False
    assert build_action.is_build is True
    assert manual_action.is_manual is True
    assert manual_action.is_pull is False
    assert manual_action.is_build is False
    assert manual_action.mode == ImageActionMode.MANUAL
    assert pull_action.mode == ImageActionMode.PULL
    assert build_action.mode == ImageActionMode.BUILD

def test_from_str_valid_and_invalid():
    build_action = ImageAction(ImageActionMode.BUILD)
    pull_action = ImageAction(ImageActionMode.PULL)
    manual_action = ImageAction(ImageActionMode.MANUAL)
    assert isinstance(ImageAction.from_str("PULL"), ImageAction)
    assert isinstance(ImageAction.from_str("BUILD"), ImageAction)
    assert isinstance(ImageAction.from_str("MANUAL"), ImageAction)
    assert ImageAction.from_str("INVALID") == manual_action
    assert ImageAction.from_str("") == manual_action
    assert ImageAction.from_str("PULL") == pull_action
    assert ImageAction.from_str("BUILD") == build_action
    assert ImageAction.from_str("MANUAL") == manual_action
    

def test_string_and_repr_outputs():
    build_action = ImageAction(ImageActionMode.BUILD)
    pull_action = ImageAction(ImageActionMode.PULL)
    manual_action = ImageAction(ImageActionMode.MANUAL)
    assert str(build_action) == "BUILD"
    assert str(pull_action) == "PULL"
    assert str(manual_action) == "MANUAL"
    assert repr(build_action) == "ImageAction(mode=BUILD)"
    assert repr(pull_action) == "ImageAction(mode=PULL)"
    assert repr(manual_action) == "ImageAction(mode=MANUAL)"
    
