#!/usr/bin/python
# -*- coding: utf-8 -*-

from moto.particle.base.tagset import BaseTagset
from moto.particle.base.tag import BaseTag
import pytest  # type: ignore


@pytest.fixture
def tagset_empty_instance():
    return BaseTagset()


@pytest.fixture
def tagset_instance():
    return BaseTagset(
        tags=[
            BaseTag(key="name", value="peter"),
            BaseTag(key="age", value="25"),
            BaseTag(key="gender", value="male"),
        ]
    )


def test_init_default(tagset_empty_instance):
    assert tagset_empty_instance.tags == []
    assert tagset_empty_instance.book == {}


def test_init_with_tags(tagset_instance):
    assert tagset_instance.tags == [
        BaseTag(key="name", value="peter"),
        BaseTag(key="age", value="25"),
        BaseTag(key="gender", value="male"),
    ]


def test_empty_instance_str(tagset_empty_instance):
    assert str(tagset_empty_instance) == "{}"


def test_instance_str(tagset_instance):
    assert str(tagset_instance) == "{'name': 'peter', 'age': '25', 'gender': 'male'}"


def test_empty_instance_dict(tagset_empty_instance):
    assert tagset_empty_instance.__dict__() == {}


def test_instance_dict(tagset_instance):
    assert tagset_instance.__dict__() == {
        "name": "peter",
        "age": "25",
        "gender": "male",
    }


def test_empty_instance_export(tagset_empty_instance):
    assert tagset_empty_instance.export() == {}


def test_instance_export(tagset_instance):
    assert tagset_instance.export() == {"name": "peter", "age": "25", "gender": "male"}


def test_add(tagset_instance):
    tagset_instance.add(BaseTag(key="name", value="peter"))
    assert BaseTag(key="name", value="peter") in tagset_instance.tags
    assert "name" in tagset_instance.book
    assert tagset_instance.book["name"] == "peter"

    tagset_instance.add(BaseTag(key="phone", value="123123123"))
    assert BaseTag(key="phone", value="123123123") in tagset_instance.tags
    assert "phone" in tagset_instance.book
    assert tagset_instance.book["phone"] == "123123123"


def test_remove(tagset_instance):
    tagset_instance.add(BaseTag(key="phone", value="123123123"))
    tagset_instance.remove(BaseTag(key="phone", value="123123123"))
    assert "phone" not in tagset_instance.book
    assert BaseTag(key="phone", value="123123123") not in tagset_instance.tags


def test_get(tagset_instance):
    tagset_instance.add(BaseTag(key="phone", value="123123123"))
    assert tagset_instance.get("phone") == BaseTag(key="phone", value="123123123")
    assert tagset_instance.get("email") == None


def test_update(tagset_instance):
    tagset_instance.add(BaseTag(key="phone", value="123123123"))
    tagset_instance.update(key="phone", value="321321321")
    assert tagset_instance.get("phone") == BaseTag(key="phone", value="321321321")

    tagset_instance.update(
        tag=BaseTag(
            key="email",
            value="123123123@qq.com",
        )
    )
    assert tagset_instance.get("phone") == BaseTag(key="phone", value="321321321")
    assert tagset_instance.get("email") == BaseTag(
        key="email",
        value="123123123@qq.com",
    )

    tagset_instance.update(key="address", value="abc street")
    assert tagset_instance.get("address") == BaseTag(key="address", value="abc street")
