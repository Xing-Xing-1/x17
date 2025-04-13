- **Documentation**
    - **Name**: `BasePlatform`
    - **Path**: `particle/base/platform.py`
    - **Module**: `particle/base`
    - **Type**
        - **Functionalities**: `[]`
        - **Structures**: `[]`
        - **Roles**: `[]`
    - **Parent**
        - **Parents**: `[]`
    - **Ref**
        - **Refs**: `['enum', 'logging', 'os', 'pangu.particle.base.platform_status', 'platform', 'socket', 'sys', 'typing']`
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
        - **Type**: `str`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `config`
        - **Type**: `Optional[Dict[str, Any]]`
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
            - `name`: `str`, ``
            - `config`: `Optional[Dict[str, Any]]`, ``



    - `_setup_logger`


        - **Returns**
            - `logging.Logger`: ``


    - `detect_environment`


        - **Returns**
            - `Dict[str, Any]`: ``


    - `_is_docker`


        - **Returns**
            - `bool`: ``


    - `load_config`

        - **Params**
            - `path`: `Optional[str]`, ``
            - `env_prefix`: `Optional[str]`, ``



    - `register_plugin`

        - **Params**
            - `name`: `str`, ``
            - `plugin`: `Any`, ``



    - `get_plugin`

        - **Params**
            - `name`: `str`, ``

        - **Returns**
            - `Any`: ``


    - `initialize`




    - `shutdown`




    - `is_ready`


        - **Returns**
            - `bool`: ``



---

- **Static Methods**
    - None

---

- **Class Methods**
    - None
