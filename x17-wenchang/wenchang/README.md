# Wenchang 文昌 · 神掌书吏，注籍乾坤

> A structured documentation engine for Python AST, powered by tradition, clarity, and semantic analysis.

---

## Inspiration
文昌帝君，全名“梓潼文昌帝君”，为中国神话中掌文运、注禄命、管籍录之神。传说他主张：
> “善书者昌，善学者贵，善记者寿。”

## Project Overview

**Wenchang** is a documentation and introspection engine designed to parse, structure, and export Python code components (functions, classes, modules, etc.) into semi-structured formats such as JSON, Markdown, or reStructuredText (reST). It enables both human-readable and machine-readable outputs, ideal for automated knowledge systems, developer tools, and static documentation pipelines (e.g., Sphinx).

The project draws its name and spirit from **文昌帝君**, the Taoist god of wisdom, literature, and academic success — symbolizing clarity, structure, and meaningful record-keeping.

---

## Core Features

- **AST-to-Structure Engine**: Convert Python files into rich node trees (functions, classes, comments, arguments, etc.)
- **Semantic Model**: Normalize code into `NodeType`, with recursive, typed node relationships
- **Export Formats**: Export to JSON / Markdown / reST (Sphinx-ready)
- **Comment & Docstring Parsing**: Extract and normalize inline documentation
- **CLI Support** *(Coming soon)*: `shuli build`, `shuli push`, etc.

---

## Installation

This module is part of the `x17` ecosystem. You can install it via:

```bash
pip install x17-shuli
```

## Quick Start
```
from shuli.resource.python.pymodule import PyModule

code = """
def greet(name):
    # say hello
    return f"Hello, {name}"
"""

import ast
tree = ast.parse(code)
module = PyModule.from_ast(tree, source_lines=code.splitlines())[0]
print(module.export())
```

## Project Structure

wenchang/
├── resource/
│   └── python/
│       ├── pyfunction.py
│       ├── pyclass.py
│       ├── pymodule.py
│       └── ...
├── base/
│   ├── nodetype.py
│   └── ...
└── cli/
    └── build.py (planned)