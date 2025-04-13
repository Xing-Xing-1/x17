- **Documentation**
    - **Name**: `ClassParser`
    - **Path**: `doc/gen/parser.py`
    - **Module**: `doc/gen`
    - **Type**
        - **Functionalities**: `[]`
        - **Structures**: `[]`
        - **Roles**: `[]`
    - **Parent**
        - **Parents**: `['ParserBase']`
    - **Ref**
        - **Refs**: `['ast', 'base', 'pathlib', 'typing']`
    - **Desc**
        - `Parses a Python file to extract class-level metadata and structure.`
    - **Usage**
        ```python
        
        ```
    - **Thread Safe**: `False`
    - **Mutable**: `False`
    - **Lifecycle**: `[]`
    - **Design Patterns**
        - `[]`
    - **Deprecation**: `False`
    - **Author**: ``

---

- **Class Parameters**
    - None

---

- **Attributes**
    - None

---

- **Instance Methods**
    - `parse`


        - **Returns**
            - `List[Dict[str, Any]]`: ``


    - `_get_annotation`

        - **Params**
            - `node`: `Optional[ast.AST]`, ``

        - **Returns**
            - `str`: ``


    - `_get_name`

        - **Params**
            - `node`: `ast.AST`, ``

        - **Returns**
            - `str`: ``


    - `_extract_imports`

        - **Params**
            - `tree`: `ast.Module`, ``

        - **Returns**
            - `List[str]`: ``


    - `_get_docstring`

        - **Params**
            - `node`: `Optional[ast.AST]`, ``

        - **Returns**
            - `str`: ``



---

- **Static Methods**
    - None

---

- **Class Methods**
    - None
