#!/usr/bin/python
# -*- coding: utf-8 -*-

import hashlib

"""
	Loaded all hash algorithms from hashlib and created a
	dictionary with algorithm as key and hash object as value
"""
HASH_ALGORITHMS = {algo: hashlib.new(algo) for algo in hashlib.algorithms_available}


class ConstantHash:
    def __init__(self):
        self.HASH_ALGORITHMS = {
            algo: hashlib.new(algo) for algo in hashlib.algorithms_available
        }

    def get_hash_algorithms(self):
        return self.HASH_ALGORITHMS

    def get_hash_algorithm(self, algo):
        return self.HASH_ALGORITHMS[algo]
