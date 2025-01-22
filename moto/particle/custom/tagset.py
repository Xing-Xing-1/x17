from typing import Dict, List, Optional

from moto.particle.custom.tag import BaseTag


class BaseTagset:
    """
    管理一组标签。

    """

    @classmethod
    def from_dict(cls, data):
        """
        从字典初始化标签集合。

        """
        tags = [BaseTag(key, value) for key, value in data.items()]
        return cls(tags)

    @classmethod
    def from_list(cls, data: List[dict]):
        """
        从字典列表初始化标签集合。

        """
        tags = [BaseTag.from_dict(tag) for tag in data]
        return cls(tags)

    def __init__(
        self,
        tags: Optional[List[BaseTag]] = [],
    ):
        """
        Args:
            tags (Optional[List[BaseTag]]): 标签列表。
        book (Dict[str, BaseTag]): 标签字典。
            -> key: 标签的键。
            -> value: BaseTag实例。
        """
        self.book = {tag.key: tag for tag in tags}

    def _resolve_tag(
        self,
        key: Optional[str] = None,
        value: Optional[str] = None,
        tag: Optional[BaseTag] = None,
    ):
        """
        根据 key 和 value 或 tag 参数解析标签。

        Args:
            key (Optional[str]): 标签的键。
            value (Optional[str]): 标签的值。
            tag (Optional[BaseTag]): 标签实例。

        Returns:
            Optional[BaseTag]: 解析出的标签。
        """
        if tag:
            return tag
        elif key:
            return BaseTag(key, value)
        else:
            return None

    @property
    def count(self):
        return len(self.book)

    def __len__(self):
        return len(self.book)

    def __str__(self):
        return f"BaseTagset({len(self.book)} tags)"

    def __dict__(self):
        return self.book

    def add(
        self,
        key: Optional[str] = None,
        value: Optional[str] = None,
        tag: Optional[BaseTag] = None,
    ):
        """
        添加标签。如果键已存在，则覆盖。

        Args:
            key (Optional[str]): 标签的键。
            value (Optional[str]): 标签的值。
            tag (Optional[BaseTag]): 标签实例。
        """
        resolved_tag = self._resolve_tag(key, value, tag)
        if resolved_tag:
            self.book[resolved_tag.key] = resolved_tag

    def remove(
        self,
        key: Optional[str] = None,
        value: Optional[str] = None,
        tag: Optional[BaseTag] = None,
    ):
        """
        删除标签。

        Args:
            key (Optional[str]): 标签的键。
            value (Optional[str]): 标签的值。
            tag (Optional[BaseTag]): 标签实例。
        """
        resolved_tag = self._resolve_tag(key, value, tag)
        if resolved_tag and resolved_tag.key in self.book:
            del self.book[resolved_tag.key]

    def export(self):
        return {tag.key: tag.value for tag in self.book.values()}

    def get(
        self,
        key: Optional[str] = None,
        value: Optional[str] = None,
        tag: Optional[BaseTag] = None,
        case_insensitive: bool = False,
    ):
        """
        Args:
            key (Optional[str]): 标签的键。
            value (Optional[str]): 标签的值。
            tag (Optional[BaseTag]): 标签实例。
            case_insensitive (bool): 是否忽略大小写。
        Returns:
            Optional[BaseTag]: 匹配的标签，未找到时返回 None。
        """
        if tag:
            return self.book.get(tag.key) if tag.key in self.book else None

        for t_key, t_value in self.book.items():
            key_match = (
                (key is None or t_key.lower() == key.lower())
                if case_insensitive
                else (key is None or t_key == key)
            )
            value_match = (
                (value is None or t_value.value.lower() == value.lower())
                if case_insensitive
                else (value is None or t_value.value == value)
            )

            if key_match and value_match:
                return t_value
        return None

    def update(
        self,
        key: Optional[str] = None,
        value: Optional[str] = None,
        tag: Optional[BaseTag] = None,
        tagset: Optional["BaseTagset"] = None,
    ):
        """
        更新标签。如果键存在则覆盖，否则添加。

        Args:
            key (Optional[str]): 标签的键。
            value (Optional[str]): 标签的值。
            tag (Optional[BaseTag]): 标签实例。
        """
        resolved_tag = self._resolve_tag(key, value, tag)
        if resolved_tag:
            self.book[resolved_tag.key] = resolved_tag
        elif tagset:
            self.merge(tagset)

    def list_tags(self):
        """
        列出所有标签的键。

        """
        return list(self.book.keys())

    def to_list(self):
        """
        将标签集合导出为字典列表。
        """
        return [tag.export() for tag in self.book.values()]

    def merge(self, tagset: "BaseTagset"):
        """
        合并另一个标签集合。
        """
        for tag in tagset.book.values():
            self.update(tag=tag)
