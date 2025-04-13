- **Documentation**
    - **Name**: `Url`
    - **Path**: `particle/remote/url.py`
    - **Module**: `particle/remote`
    - **Type**
        - **Functionalities**: `[]`
        - **Structures**: `[]`
        - **Roles**: `[]`
    - **Parent**
        - **Parents**: `[]`
    - **Ref**
        - **Refs**: `['typing', 'urllib.parse']`
    - **Desc**
        - `RemoteURL 是用于远程访问资源的统一地址抽象，支持：
- 从字符串解析 URL
- 拼接 path、添加 query 参数
- 导出为标准 URL 字符串或结构化字典`
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
    - `url`
        - **Type**: `Any`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `scheme`
        - **Type**: `str`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `host`
        - **Type**: `str`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `port`
        - **Type**: `Optional[int]`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `path`
        - **Type**: `str`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `query`
        - **Type**: `Optional[Dict[str, Any]]`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `user`
        - **Type**: `Optional[str]`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `password`
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
            - `url`: `Any`, ``
            - `scheme`: `str`, ``
            - `host`: `str`, ``
            - `port`: `Optional[int]`, ``
            - `path`: `str`, ``
            - `query`: `Optional[Dict[str, Any]]`, ``
            - `user`: `Optional[str]`, ``
            - `password`: `Optional[str]`, ``



    - `link`


        - **Returns**
            - `str`: ``


    - `attr`


        - **Returns**
            - `list[str]`: ``


    - `dict`


        - **Returns**
            - `dict`: ``


    - `__repr__`




    - `__str__`




    - `__truediv__`

        - **Params**
            - `segment`: `str`, ``

        - **Returns**
            - `'Url'`: `Url`


    - `__add__`

        - **Params**
            - `other`: `str`, ``

        - **Returns**
            - `'Url'`: `Url`


    - `__radd__`

        - **Params**
            - `other`: `str`, ``

        - **Returns**
            - `'Url'`: `Url`


    - `join_path`


        - **Returns**
            - `'Url'`: `Url`


    - `join_querys`

        - **Params**
            - `query`: `Dict[str, Any]`, ``

        - **Returns**
            - `'Url'`: `Url`


    - `join_query`

        - **Params**
            - `key`: `str`, ``
            - `value`: `Any`, ``

        - **Returns**
            - `'Url'`: `Url`


    - `remove_query`

        - **Params**
            - `key`: `str`, ``

        - **Returns**
            - `'Url'`: `Url`


    - `parent`


        - **Returns**
            - `'Url'`: `Url`


    - `redact`


        - **Returns**
            - `'Url'`: `Url`


    - `export`


        - **Returns**
            - `Dict[str, Any]`: ``



---

- **Static Methods**
    - None

---

- **Class Methods**
    - `from_str`
        
        - **Params**
            - `url_str`: `str`, ``

        - **Returns**
            - `'Url'`: `Url`

    - `from_dict`
        
        - **Params**
            - `data`: `Dict[str, Any]`, ``

        - **Returns**
            - `'Url'`: `Url`

