from typing import Optional

class BaseTag:
    """
        表示单个标签。

    """

    @classmethod
    def from_dict(cls, data: dict):
        """
            从字典初始化标签。
            Args:
                data (dict): 包含键和值的字典。
        """
        return cls(data.get("key", ""), data.get("value", ""))

    def __init__(self, key: str, value: str = ""):
        self.key = key
        self.value = value

    def __str__(self):
        return f"BaseTag(key={self.key}, value={self.value})"

    def __dict__(self):
        return {self.key: self.value}

    def __eq__(self, other):
        return isinstance(other, BaseTag) and self.key == other.key and self.value == other.value

    def __ne__(self, other):
        return not self.__eq__(other)
    
    def get_key(self):
        """
            获取标签的键。
            
        """
        return self.key
    
    def get_value(self):
        """
            获取标签的值。
            
        """
        return self.value


    def update(self, key: Optional[str] = None, value: Optional[str] = None):
        """
            更新标签的键和值。
            
        """
        if key:
            self.key = key
        if value:
            self.value = value

    def export(self):
        """
            导出标签为字典。

        """
        return self.__dict__()