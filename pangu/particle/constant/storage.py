#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
	Storage unit constants in bytes and conversions
	Default unit = byte
	Defualt ratio = 1024

"""
BYTE = 1
STORAGE_RATIO = 1024
STORAGE_UNIT_TABLE = {
    "b": BYTE,
    "byte": BYTE,
    "kb": BYTE * STORAGE_RATIO,
    "kilobyte": BYTE * STORAGE_RATIO,
    "mb": BYTE * STORAGE_RATIO**2,
    "megabyte": BYTE * STORAGE_RATIO**2,
    "gb": BYTE * STORAGE_RATIO**3,
    "gigabyte": BYTE * STORAGE_RATIO**3,
    "tb": BYTE * STORAGE_RATIO**4,
    "terabyte": BYTE * STORAGE_RATIO**4,
    "pb": BYTE * STORAGE_RATIO**5,
    "petabyte": BYTE * STORAGE_RATIO**5,
}


class ConstantStorage:
    def __init__(
        self,
        ratio=STORAGE_RATIO,
        byte=BYTE,
    ):
        self.BYTE = BYTE if byte is None else byte
        self.STORAGE_RATIO = STORAGE_RATIO if ratio is None else ratio
        self.STORAGE_UNIT_TABLE = {
            "b": self.BYTE,
            "byte": self.BYTE,
            "kb": self.BYTE * self.STORAGE_RATIO,
            "kilobyte": self.BYTE * self.STORAGE_RATIO,
            "mb": self.BYTE * self.STORAGE_RATIO**2,
            "megabyte": self.BYTE * self.STORAGE_RATIO**2,
            "gb": self.BYTE * self.STORAGE_RATIO**3,
            "gigabyte": self.BYTE * self.STORAGE_RATIO**3,
            "tb": self.BYTE * self.STORAGE_RATIO**4,
            "terabyte": self.BYTE * self.STORAGE_RATIO**4,
            "pb": self.BYTE * self.STORAGE_RATIO**5,
            "petabyte": self.BYTE * self.STORAGE_RATIO**5,
        }

    def set_ratio(self, ratio):
        byte = self.BYTE
        self.__init__(ratio, byte)

    def set_byte(self, byte):
        ratio = self.STORAGE_RATIO
        self.__init__(ratio, byte)

    def set(self, ratio, byte):
        self.__init__(ratio, byte)
