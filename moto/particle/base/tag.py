class BaseTag:
    @classmethod
    def from_dict(cls, dict):
        return cls(dict["key"], dict["value"])

    # Init method
    def __init__(
        self,
        key="",
        value="",
    ):
        self.key = key
        self.value = value

    def __str__(self):
        return f"{self.key}: {self.value}"

    def __dict__(self):
        return {self.key: self.value}

    def __eq__(self, other):
        return self.key == other.key and self.value == other.value

    def __ne__(self, other):
        return not self.__eq__(other)

    def update(self, key=None, value=None):
        if key:
            self.key = key
        if value:
            self.value = value

    def get_key(self):
        return self.key

    def get_value(self):
        return self.value

    def export(self):
        return self.__dict__()
