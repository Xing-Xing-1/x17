#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import shutil

from moto.particle.base.file import BaseFile
from moto.particle.datestamp import datestamp
from moto.particle.storage import storage


class File(BaseFile):
    def __init__(self, path=None, is_strict=False):
        super(File, self).__init__(
            path,
            is_strict,
        )
        self.content = None

    """
	Base methods

	"""

    def __str__(self):
        return super().__str__()

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
