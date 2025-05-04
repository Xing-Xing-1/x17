- **Documentation**
    - **Name**: `LogGroup`
    - **Path**: `particle/log/log_group.py`
    - **Module**: `particle/log`
    - **Type**
        - **Functionalities**: `[]`
        - **Structures**: `[]`
        - **Roles**: `[]`
    - **Parent**
        - **Parents**: `[]`
    - **Ref**
        - **Refs**: `['pangu.particle.datestamp', 'pangu.particle.log.log_core', 'pangu.particle.log.log_event', 'pangu.particle.log.log_stream', 'pangu.particle.text.id', 'queue', 'threading', 'typing']`
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
    - `core`
        - **Type**: `Optional[LogCore]`
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
            - `core`: `Optional[LogCore]`, ``



    - `attr`


        - **Returns**
            - `list[str]`: ``


    - `dict`


        - **Returns**
            - `dict[str, str]`: ``


    - `__repr__`




    - `__str__`




    - `register_stream`

        - **Params**
            - `stream`: `LogStream`, ``



    - `receive`

        - **Params**
            - `stream_name`: `str`, ``
            - `event`: `LogEvent`, ``



    - `_consume`




    - `export`


        - **Returns**
            - `Dict[str, List[Dict[str, Any]]]`: ``



---

- **Static Methods**
    - None

---

- **Class Methods**
    - None
