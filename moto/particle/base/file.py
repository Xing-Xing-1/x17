from moto.particle.base.item import BaseItem


class BaseFile(BaseItem):
    def __init__(
        self,
        path: str = "",
        strict: bool = False,
    ):
        super().__init__(
            path=path,
            strict=strict,
        )
        if self.exists and not self.is_file:
            raise ValueError(f"The path '{self.path}' is not a file.")

        if self.path:
            self.suffix = self.path.suffix  # Single extension
            self.suffixes = self.path.suffixes  # All extensions
        else:
            self.suffix = None
            self.suffixes = None

    def __str__(self):
        return f"BaseFile(name={self.name}, path={self.get_path(as_str=True)})"

    def __dict__(self):
        result = super().__dict__()
        result.update(
            {
                "suffix": self.suffix,
                "suffixes": self.suffixes,
            }
        )
        return result

    def get_suffix(
        self,
        lower: bool = True,
    ):
        if self.suffix:
            return self.suffix.lower() if lower else self.suffix
        else:
            return None
