from os.path import abspath
from pathlib import Path

from moto.particle.datestamp import datestamp

class File:
    def __init__(
        self,
        path: str = "",
        strict: bool = False,
    ):
        if path:
            self.path = Path(path)
            try:
                self.full_path = self.path.resolve(strict=strict)
            except Exception:
                self.full_path = Path(abspath(self.path))
            self.name = self.path.name
            self.suffix = self.path.suffix
            self.exists = self.path.exists()
        else:
            self.path = None
            self.full_path = None
            self.name = None
            self.extension = None
            self.suffix = None
            self.exists = False

        current_datestamp = datestamp()
        self.created_at = current_datestamp
        self.updated_at = current_datestamp

    def set(
        self,
        path: str = "",
    ):
        self.__init__(
            path=path,
        )

    def exists(self):
        return self.path.exists()

    def get_name(self):
        return self.name

    def get_path(
        self,
        as_str: bool = False,
        as_posix: bool = True,
    ):
        if self.path and as_str:
            return self.path.as_posix() if as_posix else str(self.path)
        else:
            return self.path

    def get_fullpath(
        self,
        as_str: bool = False,
        as_posix: bool = True,
    ):
        if self.path and as_str:
            return self.full_path.as_posix() if as_posix else str(self.path)
        else:
            return self.full_path

    def get_suffix(self):
        return self.suffix

    def update_datestamp(
        self,
        updated_at: datestamp = datestamp(),
    ):
        self.updated_at = updated_at
