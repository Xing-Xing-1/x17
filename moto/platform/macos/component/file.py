#!/usr/bin/python
# -*- coding: utf-8 -*-

from moto.particle.base.file import BaseFile
from moto.particle.datestamp import datestamp
from moto.particle.storage import storage
import shutil
import os

class File(BaseFile):
	def __init__(self, path, is_strict=False):
		super(File, self).__init__(path, is_strict,)
		self.is_file = os.path.isfile(self.path)
		self.is_dir = os.path.isdir(self.path)
		self.is_hidden = self.name.startswith('.')

		if self.exists:
			self.id = os.stat(self.path).st_ino
			self.create_at = datestamp.from_timestamp(
				os.path.getctime(self.path),
			)
			self.modify_at = datestamp.from_timestamp(
				os.path.getmtime(self.path),
			)
			self.access_at = datestamp.from_timestamp(
				os.path.getatime(self.path),
			)
			self.size = storage(
				os.path.getsize(self.path)
			)
		else:
			self.id = None
			self.create_at = None
			self.modify_at = None
			self.access_at = None
			self.size = storage(0)
			

	def __str__(self):
		return super().__str__()

	def __dict__(self):
		upper_class_dict = super(File, self).__dict__()
		upper_class_dict.update({
			"id": str(self.id),
			"create_at": str(self.create_at),
			"modify_at": str(self.modify_at),
			"access_at": str(self.access_at),
			"size": str(self.size),
			"is_file": self.is_file,
			"is_dir": self.is_dir,
			"is_hidden": self.is_hidden,
		})
		return upper_class_dict
		
	

