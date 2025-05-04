- **Documentation**
    - **Name**: `LogCore`
    - **Path**: `particle/log/log_core.py`
    - **Module**: `particle/log`
    - **Type**
        - **Functionalities**: `[]`
        - **Structures**: `[]`
        - **Roles**: `[]`
    - **Parent**
        - **Parents**: `[]`
    - **Ref**
        - **Refs**: `['pangu.particle.log.log_event', 'pangu.particle.text.id', 'queue', 'threading', 'typing']`
    - **Desc**
        - `None`
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
    - `name`
        - **Type**: `Optional[str]`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`

---

- **Attributes**
    - None

---

- **Instance Methods**
    - `__init__`

        - **Params**
            - `name`: `Optional[str]`, ``



    - `register_group`

        - **Params**
            - `group`: `'LogGroup'`, ``

        - **Returns**
            - `str`: ``


    - `push`

        - **Params**
            - `group`: `str`, ``
            - `stream`: `str`, ``
            - `event`: `LogEvent`, ``



    - `_consume`




    - `export`

        - **Params**
            - `group`: `Optional[str]`, ``
            - `stream`: `Optional[str]`, ``

        - **Returns**
            - `Any`: ``



---

- **Static Methods**
    - None

---

- **Class Methods**
    - None
