- **Documentation**
    - **Name**: `Call`
    - **Path**: `particle/remote/call.py`
    - **Module**: `particle/remote`
    - **Type**
        - **Functionalities**: `[]`
        - **Structures**: `[]`
        - **Roles**: `[]`
    - **Parent**
        - **Parents**: `[]`
    - **Ref**
        - **Refs**: `['json', 'pangu.particle.datestamp.datestamp', 'pangu.particle.duration', 'pangu.particle.log.log_event', 'pangu.particle.remote.response', 'pangu.particle.remote.url', 'time', 'typing', 'urllib.error', 'urllib.parse', 'urllib.request']`
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
    - `method`
        - **Type**: `str`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `url`
        - **Type**: `Union[str, Url]`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `headers`
        - **Type**: `Optional[Dict[str, str]]`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `query`
        - **Type**: `Optional[Dict[str, Any]]`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `body`
        - **Type**: `Optional[Union[str, bytes, dict]]`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `timeout`
        - **Type**: `int`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `retry`
        - **Type**: `int`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `interval`
        - **Type**: `Duration`
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
            - `method`: `str`, ``
            - `url`: `Union[str, Url]`, ``
            - `headers`: `Optional[Dict[str, str]]`, ``
            - `query`: `Optional[Dict[str, Any]]`, ``
            - `body`: `Optional[Union[str, bytes, dict]]`, ``
            - `timeout`: `int`, ``
            - `retry`: `int`, ``
            - `interval`: `Duration`, ``



    - `attr`


        - **Returns**
            - `list`: ``


    - `dict`


        - **Returns**
            - `Dict[str, Any]`: ``


    - `__repr__`




    - `__str__`




    - `data`
        - **Description**: Encode request body if present.


        - **Returns**
            - `bytes`: ``


    - `request`


        - **Returns**
            - `urllib.request.Request`: ``


    - `send`


        - **Returns**
            - `'Response'`: `Response`



---

- **Static Methods**
    - None

---

- **Class Methods**
    - `from_dict`
        
        - **Params**
            - `data`: `Dict[str, Any]`, ``

        - **Returns**
            - `'Call'`: `Call`

    - `from_json`
        
        - **Params**
            - `json_str`: `str`, ``

        - **Returns**
            - `'Call'`: `Call`

