import pytest
from moto.particle.custom.tag import BaseTag  # type: ignore
from moto.particle.custom.tagset import BaseTagset  # type: ignore


def test_init_empty():
    """
    测试空初始化 BaseTagset。
    """
    tagset = BaseTagset()
    assert tagset.count == 0
    assert len(tagset.book) == 0


def test_init_with_tags():
    """
    测试使用初始标签列表初始化 BaseTagset。
    """
    tags = [BaseTag("key1", "value1"), BaseTag("key2", "value2")]
    tagset = BaseTagset(tags)
    assert tagset.count == 2
    assert len(tagset.book) == 2
    assert tagset.book["key1"].value == "value1"
    assert tagset.book["key2"].value == "value2"


def test_add_with_key_value():
    """
    测试使用 key 和 value 添加标签。
    """
    tagset = BaseTagset()
    tagset.add(key="key1", value="value1")
    assert tagset.count == 1
    assert tagset.book["key1"].value == "value1"


def test_add_with_tag():
    """
    测试使用 BaseTag 实例添加标签。
    """
    tagset = BaseTagset()
    tag = BaseTag("key1", "value1")
    tagset.add(tag=tag)
    assert tagset.count == 1
    assert tagset.book["key1"].value == "value1"


def test_remove_with_key():
    """
    测试使用 key 删除标签。
    """
    tagset = BaseTagset([BaseTag("key1", "value1")])
    tagset.remove(key="key1")
    assert tagset.count == 0


def test_remove_with_tag():
    """
    测试使用 BaseTag 实例删除标签。
    """
    tag = BaseTag("key1", "value1")
    tagset = BaseTagset([tag])
    tagset.remove(tag=tag)
    assert tagset.count == 0


def test_get_with_key():
    """
    测试通过 key 查找标签。
    """
    tagset = BaseTagset([BaseTag("key1", "value1")])
    tag = tagset.get(key="key1")
    assert tag is not None
    assert tag.key == "key1"
    assert tag.value == "value1"


def test_get_with_value():
    """
    测试通过 value 查找标签。
    """
    tagset = BaseTagset([BaseTag("key1", "value1")])
    tag = tagset.get(value="value1")
    assert tag is not None
    assert tag.key == "key1"
    assert tag.value == "value1"


def test_get_case_insensitive():
    """
    测试忽略大小写查找标签。
    """
    tagset = BaseTagset([BaseTag("Key1", "Value1")])
    tag = tagset.get(key="key1", case_insensitive=True)
    assert tag is not None
    assert tag.key == "Key1"
    assert tag.value == "Value1"


def test_update_with_key_value():
    """
    测试使用 key 和 value 更新标签。
    """
    tagset = BaseTagset([BaseTag("key1", "value1")])
    tagset.update(key="key1", value="updated_value")
    assert tagset.book["key1"].value == "updated_value"


def test_update_with_tag():
    """
    测试使用 BaseTag 实例更新标签。
    """
    tagset = BaseTagset([BaseTag("key1", "value1")])
    tagset.update(tag=BaseTag("key1", "updated_value"))
    assert tagset.book["key1"].value == "updated_value"


def test_list_tags():
    """
    测试列出所有标签的键。
    """
    tagset = BaseTagset([BaseTag("key1", "value1"), BaseTag("key2", "value2")])
    assert tagset.list_tags() == ["key1", "key2"]


def test_to_list():
    """
    测试将标签集合导出为字典列表。
    """
    tagset = BaseTagset([BaseTag("key1", "value1"), BaseTag("key2", "value2")])
    result = tagset.to_list()
    expected = [{"key1": "value1"}, {"key2": "value2"}]
    assert result == expected


def test_export():
    """
    测试导出标签集合为字典。
    """
    tagset = BaseTagset([BaseTag("key1", "value1"), BaseTag("key2", "value2")])
    result = tagset.export()
    assert result == {
        "key1": "value1",
        "key2": "value2",
    }