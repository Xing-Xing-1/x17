- **Documentation**
    - **Name**: `AwsClient`
    - **Path**: `aws/base/aws_client.py`
    - **Module**: `aws/base`
    - **Type**
        - **Functionalities**: `[]`
        - **Structures**: `[]`
        - **Roles**: `[]`
    - **Parent**
        - **Parents**: `[]`
    - **Ref**
        - **Refs**: `['pangu.particle.log.log_group', 'pangu.particle.log.log_stream', 'typing']`
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
    - `account_id`
        - **Type**: `Optional[str]`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `service`
        - **Type**: `Optional[str]`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `region`
        - **Type**: `Optional[str]`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `plugin`
        - **Type**: `Optional[Dict[str, Any]]`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `log_group`
        - **Type**: `Optional[LogGroup]`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`

---

- **Attributes**
    - `REGION_NAME`
        - **Type**: `Any`
        - **Desc**: ``
    - `MAX_PAGINATE`
        - **Type**: `Any`
        - **Desc**: ``

---

- **Instance Methods**
    - `__init__`
        - **Description**: Initialize the AwsClient instance.

        - **Params**
            - `account_id`: `Optional[str]`, ``
            - `service`: `Optional[str]`, ``
            - `region`: `Optional[str]`, ``
            - `plugin`: `Optional[Dict[str, Any]]`, ``
            - `log_group`: `Optional[LogGroup]`, ``



    - `register_plugin`

        - **Params**
            - `name`: `str`, ``
            - `plugin`: `Any`, ``



    - `__str__`




    - `__repr__`




    - `__dict__`




    - `log`

        - **Params**
            - `level`: `str`, ``
            - `message`: `str`, ``




---

- **Static Methods**
    - None

---

- **Class Methods**
    - `get_region`
        

        - **Returns**
            - `str`: ``

    - `get_max_paginate`
        

        - **Returns**
            - `int`: ``

    - `set_default`
        
        - **Params**
            - `region`: `Any`, ``
            - `max_paginate`: `Any`, ``


