import os
from os.path import abspath
from pathlib import Path

from moto.particle.datestamp import datestamp
from moto.particle.storage import storage


class BaseItem:
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
            self.exists = self.path.exists()
        else:
            self.path = None
            self.full_path = None
            self.name = None
            self.exists = False

        if self.exists:
            self.is_file = os.path.isfile(self.path)
            self.is_dir = os.path.isdir(self.path)
            self.dirname = os.path.dirname(self.path)
            self.size = storage(os.path.getsize(self.path))
            self.is_hidden = self.name.startswith(".")
            self.permission = {
                "r": os.access(self.path, os.R_OK),
                "w": os.access(self.path, os.W_OK),
                "x": os.access(self.path, os.X_OK),
            }
        else:
            self.dirname = None
            self.size = storage(0)
            self.is_file = None
            self.is_dir = None
            self.is_hidden = None
            self.permission = None

        try:
            self.id = os.stat(self.path).st_ino
        except Exception:
            self.id = None

    """
        Properties for BaseItem

    """

    @property
    def create_at(self):
        if self.exists:
            return datestamp.from_timestamp(
                os.path.getctime(self.path),
            )
        else:
            return None

    @property
    def modify_at(self):
        if self.exists:
            return datestamp.from_timestamp(
                os.path.getmtime(self.path),
            )
        else:
            return None

    @property
    def access_at(self):
        if self.exists:
            return datestamp.from_timestamp(
                os.path.getatime(self.path),
            )
        else:
            return None

    def __str__(self):
        return f"BaseItem(name={self.name}, path={self.get_path(as_str=True)})"

    def __dict__(self):
        return {
            "path": self.get_path(as_str=True),
            "full_path": self.get_fullpath(as_str=True),
            "name": self.get_name(),
            "exists": self.check_exists(),
            "id": str(self.id) if self.id else None,
            "create_at": str(self.create_at) if self.create_at else None,
            "modify_at": str(self.modify_at) if self.modify_at else None,
            "access_at": str(self.access_at) if self.access_at else None,
            "size": self.size.size,
            "is_file": self.is_file,
            "is_dir": self.is_dir,
            "is_hidden": self.is_hidden,
        }

    def __eq__(self, other):
        if not isinstance(other, BaseItem):
            return False
        return self.full_path == other.full_path

    """
        Get methods for BaseItem

    """

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

    def get_name(self):
        return self.name

    def get_id(self):
        return self.id

    def get_create_at(self):
        return self.create_at

    def get_modify_at(self):
        return self.modify_at

    def get_access_at(self):
        return self.access_at

    def get_size(self):
        return self.size

    def get_permission(self):
        return self.permission

    """
        Utility methods for BaseItem

    """

    def set(
        self,
        path: str = "",
    ):
        self.__init__(
            path=path,
        )

    def check_exists(self):
        return self.path.exists() if self.path else False
