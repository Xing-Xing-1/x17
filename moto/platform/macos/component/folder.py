#!/usr/bin/python
# -*- coding: utf-8 -*-

from moto.particle.base.file import BaseFile
from moto.particle.datestamp import datestamp
from moto.particle.storage import storage
import shutil
import os

class Folder:
    def __init__(self, path):
        # super(Folder, self).__init__(
        pass