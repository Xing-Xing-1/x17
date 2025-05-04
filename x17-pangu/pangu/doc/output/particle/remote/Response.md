- **Documentation**
    - **Name**: `Response`
    - **Path**: `particle/remote/response.py`
    - **Module**: `particle/remote`
    - **Type**
        - **Functionalities**: `[]`
        - **Structures**: `[]`
        - **Roles**: `[]`
    - **Parent**
        - **Parents**: `[]`
    - **Ref**
        - **Refs**: `['json', 'pangu.particle.datestamp.datestamp', 'pangu.particle.log.log_event', 'pangu.particle.remote.url', 'typing']`
    - **Desc**
        - `Represents an HTTP response.`
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
    - `status`
        - **Type**: `int`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `headers`
        - **Type**: `dict`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `body`
        - **Type**: `bytes`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `url`
        - **Type**: `str`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `error`
        - **Type**: `str`
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
            - `status`: `int`, ``
            - `headers`: `dict`, ``
            - `body`: `bytes`, ``
            - `url`: `str`, ``
            - `error`: `str`, ``



    - `attr`


        - **Returns**
            - `List[str]`: ``


    - `dict`


        - **Returns**
            - `Dict[str, Any]`: ``


    - `success`


        - **Returns**
            - `bool`: ``


    - `encoding`


        - **Returns**
            - `str`: ``


    - `text`


        - **Returns**
            - `str`: ``


    - `log`


        - **Returns**
            - `LogEvent`: ``


    - `__repr__`




    - `__str__`




    - `json`

        - **Params**
            - `check`: `Any`, ``

        - **Returns**
            - `Union[Dict[str, Any], Any]`: ``


    - `export`


        - **Returns**
            - `Dict[str, Any]`: ``



---

- **Static Methods**
    - None

---

- **Class Methods**
    - `from_dict`
        
        - **Params**
            - `data`: `Dict[str, Any]`, ``

        - **Returns**
            - `'Response'`: `Response`

    - `from_json`
        
        - **Params**
            - `json_str`: `str`, ``

        - **Returns**
            - `'Response'`: `Response`

