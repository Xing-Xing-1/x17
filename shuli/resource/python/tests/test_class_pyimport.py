# -*- coding: utf-8 -*-
import ast
from shuli.resource.python.pyimport import PyImport

test_cases = [
    ("import os", [("os", None, None, None, "os")]),
    ("import os, sys", [("os", None, None, None, "os"), ("sys", None, None, None, "sys")]),
    ("import pandas as pd", [("pandas", "pd", None, None, "pandas")]),
    ("from typing import List", [("List", None, "typing", 0, "typing.List")]),
    ("from typing import Dict as D", [("Dict", "D", "typing", 0, "typing.Dict")]),
    ("from typing import List, Dict", [
        ("List", None, "typing", 0, "typing.List"),
        ("Dict", None, "typing", 0, "typing.Dict"),
    ]),
    ("from . import something", [("something", None, None, 1, "something")]),
    ("from ..module.sub import A as Alias", [("A", "Alias", "module.sub", 2, "module.sub.A")]),
]

def test_pyimport_from_ast_variants():
    for code, expected in test_cases:
        node = ast.parse(code).body[0]
        results = PyImport.from_ast(node)
        assert len(results) == len(expected)

        for imp, (name, alias, module, level, source) in zip(results, expected):
            assert imp.name == name
            assert imp.attributes["alias"] == alias
            assert imp.attributes["module"] == module
            assert imp.attributes["level"] == level
            assert imp.attributes["source"] == source
            assert imp.type.value == "import"
    