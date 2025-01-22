#!/usr/bin/python
# -*- coding: utf-8 -*-

import pytest # type: ignore

from moto.particle.custom.tag import BaseTag  # type: ignore


def test_init_default():
    """
    测试默认初始化 BaseTag。
    """
    tag = BaseTag(key="", value="")
    assert tag.key == ""
    assert tag.value == ""

    tag = BaseTag(key="")
    assert tag.key == ""
    assert tag.value == ""


def test_init_with_key():
    """
    测试仅使用 key 初始化 BaseTag。
    """
    tag = BaseTag(key="key")
    assert tag.key == "key"
    assert tag.value == ""


def test_init_with_key_value():
    """
    测试使用 key 和 value 初始化 BaseTag。
    """
    tag = BaseTag(key="key", value="value")
    assert tag.key == "key"
    assert tag.value == "value"


def test_str():
    """
    测试 BaseTag 的字符串表示。
    """
    tag = BaseTag(key="key", value="value")
    assert str(tag) == f"BaseTag(key=key, value=value)"


def test_dict():
    """
    测试 BaseTag 的字典表示。
    """
    tag = BaseTag(key="key", value="value")
    assert tag.__dict__() == {"key": "value"}


def test_eq():
    """
    测试 BaseTag 的相等性比较。
    """
    tag1 = BaseTag(key="key", value="value")
    tag2 = BaseTag(key="key", value="value")
    assert tag1 == tag2


def test_ne():
    """
    测试 BaseTag 的不等性比较。
    """
    tag1 = BaseTag(key="key", value="value")
    tag2 = BaseTag(key="key", value="value")
    assert not tag1 != tag2


def test_update():
    """
    测试更新 BaseTag 的 key 和 value。
    """
    tag = BaseTag(key="key", value="value")
    tag.update(key="new_key", value="new_value")
    assert tag.key == "new_key"
    assert tag.value == "new_value"


def test_partial_update():
    """
    测试只更新 BaseTag 的 key 或 value。
    """
    tag = BaseTag(key="key", value="value")
    tag.update(key="new_key")
    assert tag.key == "new_key"
    assert tag.value == "value"

    tag.update(value="new_value")
    assert tag.key == "new_key"
    assert tag.value == "new_value"


def test_get_key():
    """
    测试获取 BaseTag 的 key。
    """
    tag = BaseTag(key="key", value="value")
    assert tag.get_key() == "key"


def test_get_value():
    """
    测试获取 BaseTag 的 value。
    """
    tag = BaseTag(key="key", value="value")
    assert tag.get_value() == "value"


def test_export():
    """
    测试导出 BaseTag 为字典。
    """
    tag = BaseTag(key="key", value="value")
    assert tag.export() == {"key": "value"}