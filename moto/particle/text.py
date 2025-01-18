#!/usr/bin/python
# -*- coding: utf-8 -*-

from moto.particle.constant import (
    HASH_ALGORITHMS,
)


class text:
    def __init__(self, text=""):
        self.content = text

    def __str__(self):
        return self.content

    def __dict__(self):
        return {
            "content": self.content,
        }

    def __eq__(self, other):
        return self.content == other.content

    def __ne__(self, other):
        return self.content != other.content

    def __add__(self, other):
        return text(self.content + other.content)

    def __len__(self):
        return len(self.content)

    def encode(self):
        return self.content.encode()

    def as_upper(self):
        self.content = self.content.upper()

    def as_lower(self):
        self.content = self.content.lower

    def to_upper(self):
        return text(self.content.upper())

    def to_lower(self):
        return text(self.content.lower())

    """
		Hashing:
		- get_algo(): returns the list of available algorithms
		- validate_algo(): checks if the algorithm is valid
		- as_digest(): updates the content with the hash digest
		- to_digest(): returns the hash digest

	"""

    def get_algo(self):
        return HASH_ALGORITHMS.keys()

    def validate_algo(self, algorithm: str):
        if algorithm not in HASH_ALGORITHMS:
            raise ValueError(f"Invalid algorithm: {algorithm}")
        else:
            return True

    def as_digest(
        self,
        algorithm: str = "sha256",
    ):
        self.validate_algo(algorithm)
        hash_function = HASH_ALGORITHMS[algorithm]
        hash_function.update(self.encode())
        self.content = hash_function.hexdigest()

    def to_digest(
        self,
        algorithm: str = "sha256",
    ):
        self.as_digest(algorithm)
        return text(self.content)
