from moto.particle.base.item import BaseItem # type: ignore
from moto.particle.base.file import BaseFile # type: ignore
from moto.particle.storage import storage # type: ignore
import re

class BaseFolder(BaseItem):
    def __init__(
        self,
        path: str = "",
        strict: bool = False,
    ):
        super().__init__(path, strict)

        if self.exists and not self.is_dir:
            raise NotADirectoryError(f"The path '{self.path}' is not a directory.")
    
        self._size = self.compute_size()

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        self._size = value

    def compute_size(self):
        if not self.exists:
            return storage(0)
        else:
            return storage(
                sum(f.stat().st_size for f in self.path.rglob("*") if f.is_file())
            )


    def __str__(self):
        return f"BaseFolder(name={self.name}, path={self.get_path(as_str=True)})"

    def __dict__(self):
        result = super().__dict__()
        return result


    """
    列出文件夹内容，根据条件筛选。
    
    Args:
        recursive (bool): 是否递归列出子目录内容。
        include_hidden (bool): 是否包含隐藏文件和文件夹。
        include_files (bool): 是否包含文件。
        include_folders (bool): 是否包含文件夹。
        regex_prefix (str): 文件名的前缀正则表达式。
        regex_suffix (str): 文件名的后缀正则表达式。
    
    Returns:
        list: 符合条件的 BaseItem, BaseFolder 或 BaseItem 对象列表。
    """
    def list(
            self, 
            recursive=False, 
            include_hidden=False, 
            include_files=True, 
            include_folders=True,
            name_prefix = None,
            name_suffix = None,
        ):
        if not self.exists or not self.is_dir:
            raise NotADirectoryError(f"The path '{self.path}' is not a directory.")

        iterator = self.path.rglob("*") if recursive else self.path.iterdir()

        results = []
        for item in iterator:
            try:
                if not include_hidden and item.name.startswith("."):
                    continue
                if item.is_file() and not include_files:
                    continue
                if item.is_dir() and not include_folders:
                    continue
                if name_prefix and not re.match(f"^{name_prefix}", item.name):
                    continue
                if name_suffix and not re.search(f"{name_suffix}$", item.name):
                    continue

                if item.is_file():
                    results.append(BaseFile(str(item)))
                elif item.is_dir():
                    results.append(BaseFolder(str(item)))
                else:
                    results.append(BaseItem(str(item)))
            except Exception as e: 
                # PermissionError, FileNotFoundError
                continue

        return results


    