import os
import shutil
from pathlib import Path

from moto.particle.base.item import BaseItem
from moto.particle.datestamp import datestamp
from moto.particle.storage import storage


class BaseFolder(BaseItem):
    def __init__(self, path: str = "", strict: bool = False):
        super().__init__(path, strict)

        if self.exists and not self.is_dir:
            raise NotADirectoryError(f"The path '{self.path}' is not a directory.")

        # Additional folder-specific properties
        self.is_hidden = self.name.startswith(".") if self.name else False
        self.size = self.compute_size()

    def __str__(self):
        return f"BaseFolder(name={self.name}, path={self.get_path(as_str=True)})"

    def compute_size(self):
        """
        Calculate the total size of the folder, including all contents.
        """
        if not self.exists:
            return storage(0)
        total_size = sum(f.stat().st_size for f in self.path.rglob("*") if f.is_file())
        return storage(total_size)

    def list_contents(self, include_hidden=False):
        """
        List all contents (files and subdirectories) of the folder.
        """
        if not self.exists:
            return []

        contents = [BaseItem(f) for f in self.path.iterdir()]
        if not include_hidden:
            contents = [item for item in contents if not item.is_hidden]
        return contents

    def list_files(self, include_hidden=False):
        """
        List all files in the folder.
        """
        return [
            BaseItem(f)
            for f in self.path.iterdir()
            if f.is_file() and (include_hidden or not f.name.startswith("."))
        ]

    def list_subfolders(self, include_hidden=False):
        """
        List all subdirectories in the folder.
        """
        return [
            BaseFolder(f)
            for f in self.path.iterdir()
            if f.is_dir() and (include_hidden or not f.name.startswith("."))
        ]

    def create(self):
        """
        Create the folder if it doesn't exist.
        """
        if not self.exists:
            self.path.mkdir(parents=True)
            self.exists = True

    def delete(self, recursive=False):
        """
        Delete the folder. Use recursive=True to delete non-empty folders.
        """
        if self.exists:
            if recursive:
                shutil.rmtree(self.path)
            else:
                self.path.rmdir()
            self.exists = False

    def move(self, destination: str):
        """
        Move the folder to a new location.
        """
        destination_path = Path(destination)
        shutil.move(str(self.path), str(destination_path))
        self.path = destination_path
        self.full_path = self.path.resolve(strict=False)

    def copy(self, destination: str):
        """
        Copy the folder to a new location.
        """
        destination_path = Path(destination)
        shutil.copytree(str(self.path), str(destination_path))
        return BaseFolder(str(destination_path))

    def __dict__(self):
        """
        Serialize folder attributes to a dictionary.
        """
        return {
            "path": self.get_path(as_str=True),
            "full_path": self.get_fullpath(as_str=True),
            "name": self.name,
            "exists": self.exists,
            "size": self.size.size,
            "is_hidden": self.is_hidden,
        }
