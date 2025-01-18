#!/usr/bin/python
# -*- coding: utf-8 -*-

from moto.particle.constant import (
    STORAGE_UNIT_TABLE,
)


class storage:
    def __init__(self, size: int, unit: str = "b"):
        self.size = size
        self.unit = unit

    def __str__(self):
        return f"{self.size} {self.unit}"

    def __eq__(self, other: "storage"):
        if isinstance(other, storage):
            return (
                self.size == other.to_unit(self.unit).size
                and self.unit == other.to_unit(self.unit).unit
            )
        else:
            return False

    def __add__(self, other: "storage"):
        universal_self_size = self.to_unit("b").size
        universal_other_size = other.to_unit("b").size
        return storage(
            universal_self_size + universal_other_size,
            "b",
        )

    def __sub__(self, other: "storage"):
        return storage(
            self.size - other.to_unit(self.unit).size,
            self.unit,
        )

    def __mul__(self, other: int):
        return storage(
            self.size * other,
            self.unit,
        )

    def to_unit(
        self,
        unit: str = "b",
    ):
        return storage(
            self.size * STORAGE_UNIT_TABLE[self.unit] / STORAGE_UNIT_TABLE[unit],
            unit,
        )

    def as_unit(
        self,
        unit: str = "b",
    ):
        self.size = self.size * STORAGE_UNIT_TABLE[self.unit] / STORAGE_UNIT_TABLE[unit]
        self.unit = unit

    def get_readable_size(self):
        for unit in STORAGE_UNIT_TABLE:
            if self.size < STORAGE_UNIT_TABLE[unit]:
                return self.size, unit
        return self.size, "pb"

    def to_readable(self):
        return storage(
            self.size,
            self.unit,
        ).as_readable()

    def as_readable(self):
        size, unit = self.get_readable_size()
        self.size = size
        self.unit = unit
