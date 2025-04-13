- **Documentation**
    - **Name**: `BaseTagSet`
    - **Path**: `particle/base/tagset.py`
    - **Module**: `particle/base`
    - **Type**
        - **Functionalities**: `[]`
        - **Structures**: `[]`
        - **Roles**: `[]`
    - **Parent**
        - **Parents**: `[]`
    - **Ref**
        - **Refs**: `['pangu.particle.base.tag', 'typing']`
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
    - `data`
        - **Type**: `dict`
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
            - `data`: `dict`, ``

        - **Returns**
            - `None`: `None`


    - `dict`




    - `__repr__`




    - `__str__`




    - `__getitem__`

        - **Params**
            - `key`: `str`, ``



    - `__setitem__`

        - **Params**
            - `key`: `str`, ``
            - `value`: `Union[str, int]`, ``



    - `__delitem__`

        - **Params**
            - `key`: `str`, ``



    - `__eq__`

        - **Params**
            - `other`: `Any`, ``



    - `__ne__`

        - **Params**
            - `other`: `Any`, ``



    - `__len__`




    - `list`


        - **Returns**
            - `List`: ``


    - `list_tags`


        - **Returns**
            - `List`: ``


    - `update`

        - **Params**
            - `key`: `Union[str, Dict[str, Union[str, int]]]`, ``
            - `value`: `Optional[Union[str, int]]`, ``



    - `insert`

        - **Params**
            - `key`: `Union[str, Dict[str, Union[str, int]]]`, ``
            - `value`: `Union[str, int]`, ``



    - `find`

        - **Params**
            - `key`: `str`, ``

        - **Returns**
            - `Optional[Union[str, int]]`: ``


    - `delete`

        - **Params**
            - `key`: `str`, ``



    - `find_by_prefix`

        - **Params**
            - `prefix`: `str`, ``

        - **Returns**
            - `List[BaseTag]`: ``


    - `find_by_fuzzy`

        - **Params**
            - `keyword`: `str`, ``

        - **Returns**
            - `List[BaseTag]`: ``


    - `export`


        - **Returns**
            - `Dict[str, any]`: ``



---

- **Static Methods**
    - None

---

- **Class Methods**
    - `from_dict`
        
        - **Params**
            - `data`: `dict`, ``


