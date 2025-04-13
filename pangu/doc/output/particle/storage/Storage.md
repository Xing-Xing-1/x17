- **Documentation**
    - **Name**: `Storage`
    - **Path**: `particle/storage/storage.py`
    - **Module**: `particle/storage`
    - **Type**
        - **Functionalities**: `[]`
        - **Structures**: `[]`
        - **Roles**: `[]`
    - **Parent**
        - **Parents**: `[]`
    - **Ref**
        - **Refs**: `['pangu.particle.constant.storage', 'typing']`
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
    - `size`
        - **Type**: `Optional[int]`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `unit`
        - **Type**: `LEGAL_STORAGE_UNITS`
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
            - `size`: `Optional[int]`, ``
            - `unit`: `LEGAL_STORAGE_UNITS`, ``



    - `dict`


        - **Returns**
            - `Dict[str, Union[int, str]]`: ``


    - `base`


        - **Returns**
            - `Union[int, float]`: ``


    - `get_base`


        - **Returns**
            - `Union[int, float]`: ``


    - `__repr__`


        - **Returns**
            - `str`: ``


    - `__str__`


        - **Returns**
            - `str`: ``


    - `__add__`

        - **Params**
            - `other`: `'Storage'`, ``



    - `__radd__`

        - **Params**
            - `other`: `'Storage'`, ``



    - `__eq__`

        - **Params**
            - `other`: `'Storage'`, ``



    - `__sub__`

        - **Params**
            - `other`: `'Storage'`, ``



    - `__mul__`

        - **Params**
            - `other`: `Union[int, float]`, ``



    - `as_unit`

        - **Params**
            - `unit`: `str`, ``

        - **Returns**
            - `'Storage'`: `Storage`


    - `to_unit`

        - **Params**
            - `unit`: `str`, ``

        - **Returns**
            - `'Storage'`: `Storage`


    - `get_readable_unit`

        - **Params**
            - `threshold`: `float`, ``

        - **Returns**
            - `str`: ``


    - `to_readable`


        - **Returns**
            - `'Storage'`: `Storage`


    - `as_readable`


        - **Returns**
            - `'Storage'`: `Storage`


    - `export`


        - **Returns**
            - `Dict[str, Union[any]]`: ``



---

- **Static Methods**
    - None

---

- **Class Methods**
    - None
