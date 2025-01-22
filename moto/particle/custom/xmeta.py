import json
import os
from os.path import abspath
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from moto.particle.custom.tag import BaseTag
from moto.particle.custom.tagset import BaseTagset
from moto.particle.datestamp import datestamp
from moto.particle.storage import storage


class XMeta:
    """
    管理 .xmeta 文件的类。
    用于存储文件或目录的元数据。

    """

    def __init__(
        self,
        item_path: str = "",
        strict=False,
    ):
        """
        初始化 XMeta 实例。

        Args:
            item_path (str): 源文件或目录路径。
            strict (bool): 是否严格解析路径。
        """
        # 源文件或目录路径信息
        self.src_path = Path(item_path)
        self.src_parent_path = self.src_path.parent
        self.src_exists = self.src_path.exists()
        self.src_is_file = self.src_path.is_file()
        self.src_is_dir = self.src_path.is_dir()
        self.src_name = self.src_path.name
        self.src_suffix = self.src_path.suffix
        self.src_full_path = self._resolve_path(self.src_path, strict)

        # 元数据文件路径信息
        if self.src_is_file:
            self.path = Path(
                os.path.join(self.src_parent_path.as_posix(), f".{self.src_name}.xmeta")
            )
        else:
            self.path = Path(
                os.path.join(self.src_path.as_posix(), f".{self.src_name}.xmeta")
            )
        self.parent_path = self.path.parent
        self.full_path = self._resolve_path(self.path, strict)
        self.name = self.path.name
        self.suffix = self.path.suffix
        self.suffixes = self.path.suffixes
        self.exists = os.path.exists(self.path)

        # 加载或生成元数据
        if self.exists and self.src_exists:
            self.data = self.read()
        else:
            self.data = self.generate()

    @staticmethod
    def _resolve_path(path: Path, strict: bool):
        """
        解析路径为绝对路径。

        Args:
            path (Path): 输入路径。
            strict (bool): 是否严格解析。
        Returns:
            Path: 解析后的绝对路径。
        """
        try:
            return path.resolve(strict=strict)
        except Exception:
            return Path(abspath(path))

    # 属性：源文件的元数据
    @property
    def src_size(self):
        if not self.src_exists:
            return storage(0)
        else:
            if self.src_is_dir:
                return storage(
                    sum(
                        f.stat().st_size
                        for f in self.src_path.rglob("*")
                        if f.is_file()
                    )
                )
            else:
                return storage(os.path.getsize(self.src_path))

    @property
    def src_create_at(self):
        return (
            datestamp.from_timestamp(os.path.getctime(self.src_path))
            if self.src_exists
            else None
        )

    @property
    def src_modify_at(self):
        return (
            datestamp.from_timestamp(os.path.getmtime(self.src_path))
            if self.src_exists
            else None
        )

    @property
    def src_access_at(self):
        return (
            datestamp.from_timestamp(os.path.getatime(self.src_path))
            if self.src_exists
            else None
        )

    @property
    def src_id(self):
        try:
            return os.stat(self.src_path).st_ino
        except Exception:
            return None

    def __str__(self):
        return f"XMeta(name={self.name}, path={self.path})"

    def __dict__(self):
        return {
            "name": self.name,
            "path": self.path,
            "suffix": self.suffix,
            "exists": self.exists,
        }

    def generate(self):
        return {
            "path": self.src_path.as_posix(),
            "full_path": self.src_full_path.as_posix(),
            "name": self.src_name,
            "suffix": self.src_suffix,
            "exists": self.src_exists,
            "id": self.src_id,
            "create_at": self.src_create_at,
            "modify_at": self.src_modify_at,
            "access_at": self.src_access_at,
            "size": self.src_size.size,
            "metadata": {
                "comment": "",
                "tagset": {},
            },
        }

    def export(self):
        return {
            "path": self.src_path.as_posix(),
            "full_path": self.src_full_path.as_posix(),
            "name": self.src_name,
            "suffix": self.src_suffix,
            "exists": self.src_exists,
            "id": self.src_id,
            "create_at": str(self.src_create_at),
            "modify_at": str(self.src_modify_at),
            "access_at": str(self.src_access_at),
            "size": self.src_size.size,
            "metadata": self.data.get("metadata", {}),
        }

    def read(self):
        """
        读取 .xmeta 文件内容。

        Returns:
            Dict[str, Any]: 元数据内容。
        """
        if not self.src_exists:
            raise FileNotFoundError(f"Item {self.src_path} does not exist.")
        else:
            with open(self.path, "r", encoding="utf-8") as f:
                return json.load(f)

    def write(self):
        """
        将当前元数据写入 .xmeta 文件。
        """
        if not self.src_exists:
            raise FileNotFoundError(f"Item {self.src_path} does not exist.")
        else:
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(self.export(), f, indent=4)

    def update(self, key: str, value: Any):
        self.data["metadata"][key] = value
        self.write()

    def update_tagset(
        self,
        tagset: dict = None,
        tag: BaseTag = None,
        key: str = None,
        value: Any = None,
    ):
        tagset_obj = BaseTagset.from_dict(
            self.data.get("metadata", {}).get("tagset", {})
        )
        print(tagset_obj)
        tagset_obj.update(tag=tag, key=key, value=value, tagset=tagset)
        self.data["metadata"]["tagset"] = tagset_obj.export()
        self.write()

    def comment(self, comment: str = ""):
        self.update("comment", comment)
        self.write()

    def delete(self):
        """
        删除 .xmeta 文件。

        """
        if self.exists and self.src_exists:
            os.remove(self.path)
        self.__init__(self.src_path)
