# -*- coding: utf-8 -*-
from enum import Enum
from typing import Any, Dict, List, Optional


class NodeType(Enum):
    MODULE = "module"
    CLASS = "class"
    FUNCTION = "function"
    IMPORT = "import"
    COMMENT = "comment"
    CODEBLOCK = "codeblock"
    ARGUMENT = "argument"
    OTHERS = "others"
