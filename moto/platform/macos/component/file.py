#!/usr/bin/python
# -*- coding: utf-8 -*-

from moto.particle.base.file import BaseFile
from moto.particle.datestamp import datestamp
from moto.particle.storage import storage
import shutil
import os


class File(BaseFile):
    def __init__(self, path=None, is_strict=False):
        super(File, self).__init__(
            path,
            is_strict,
        )
        self.content = None
        if self.exists:
            self.is_file = os.path.isfile(self.path)
            self.is_dir = os.path.isdir(self.path)
            if self.is_dir:
                raise IsADirectoryError(f"{self.path} is a directory")

            self.id = os.stat(self.path).st_ino
            self.dirname = os.path.dirname(self.path)
            self.create_at = datestamp.from_timestamp(
                os.path.getctime(self.path),
            )
            self.modify_at = datestamp.from_timestamp(
                os.path.getmtime(self.path),
            )
            self.access_at = datestamp.from_timestamp(
                os.path.getatime(self.path),
            )
            self.size = storage(os.path.getsize(self.path))
            self.is_hidden = self.name.startswith(".")
        else:
            self.id = None
            self.dirname = None
            self.create_at = None
            self.modify_at = None
            self.access_at = None
            self.size = storage(0)
            self.is_file = None
            self.is_dir = None
            self.is_hidden = None

    """
	Base methods

	"""

    def __str__(self):
        return super().__str__()

    def __dict__(self):
        upper_class_dict = super(File, self).__dict__()
        upper_class_dict.update(
            {
                "id": str(self.id) if self.id else None,
                "create_at": str(self.create_at) if self.create_at else None,
                "modify_at": str(self.modify_at) if self.modify_at else None,
                "access_at": str(self.access_at) if self.access_at else None,
                "size": str(self.size),
                "is_file": self.is_file,
                "is_dir": self.is_dir,
                "is_hidden": self.is_hidden,
            }
        )
        return upper_class_dict

    def set(self, content):
        self.content = content

    """
	Read methods 
	
	"""

    def read(self, mode="r"):
        if not self.exists:
            return self.content
        else:
            with open(self.path, mode) as file:
                self.content = file.read()
                return self.content

    def read_bytes(self):
        return self.read("rb")

    def read_text(self):
        return self.read("r")

    """
	Write methods

	"""

    def write(self, data, mode="w"):
        with open(self.path, mode) as file:
            file.write(
                data,
            )
        self.__init__(self.path)

    def write_bytes(self, data):
        self.write(data, "wb")

    def write_text(self, data):
        self.write(data, "w")

    def load_bytes(self, mode="rb"):
        self.content = self.read_bytes(
            mode=mode,
        )

    def load_text(self, mode="r"):
        self.content = self.read_text(mode=mode)

    """
	Operation methods

	"""

    def copy(self, target_path, force=False):
        destination = (
            os.path.join(target_path, self.name)
            if os.path.isdir(target_path)
            else target_path
        )
        if not force and os.path.exists(destination):
            raise FileExistsError(f"File {destination} already exists")

        os.makedirs(os.path.dirname(destination), exist_ok=True)
        shutil.copy(self.path, destination)
        return File(destination)

    def copy_into(self, obj: "File", force=False):
        if not force and obj.content is not None:
            raise FileExistsError(f"Target file {obj.path} already contains content")

        obj.set(self.content)
        obj.write(self.content)
        return obj

    def move(self, target_path, force=False):
        destination = (
            os.path.join(target_path, self.name)
            if os.path.isdir(target_path)
            else target_path
        )
        if not force and os.path.exists(destination):
            raise FileExistsError(f"File {destination} already exists")

        os.makedirs(os.path.dirname(destination), exist_ok=True)
        os.rename(self.path, destination)
        self.__init__(destination)

    def delete(self, force=False):
        if not self.exists:
            if force:
                return False
            else:
                raise FileNotFoundError(f"File {self.path} does not exist")

        os.remove(self.path)
        self.__init__(self.path)

    def rename(self, name):
        new_path = os.path.join(self.dirname, name)
        if not self.exists:
            raise FileNotFoundError(f"File {self.path} does not exist")

        if os.path.exists(new_path):
            raise FileExistsError(f"File {name} already exists in {self.dirname}")

        os.rename(self.path, new_path)
        self.__init__(new_path)
