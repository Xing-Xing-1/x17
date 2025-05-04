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
        - **Refs**: `['jmespath', 'pangu.particle.log.log_group', 'pangu.particle.log.log_stream', 'typing']`
    - **Desc**
        - `Base class for AWS clients.
This class provides a common interface for AWS clients, including logging and plugin registration.
Normally set the log module to log group.`
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
    - `max_paginate`
        - **Type**: `Optional[int]`
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

        - **Params**
            - `account_id`: `Optional[str]`, ``
            - `service`: `Optional[str]`, ``
            - `region`: `Optional[str]`, ``
            - `plugin`: `Optional[Dict[str, Any]]`, ``
            - `log_group`: `Optional[LogGroup]`, ``
            - `max_paginate`: `Optional[int]`, ``



    - `register_plugin`
        - **Description**: Register a plugin to the client.

        - **Params**
            - `name`: `str`, ``
            - `plugin`: `Any`, ``



    - `__str__`




    - `__repr__`




    - `dict`




    - `log`
        - **Description**: Log a message to the log stream.

        - **Params**
            - `message`: `str`, ``
            - `level`: `str`, ``



    - `pop_list`
        - **Description**: Pop out a list of data by index.
When the index is out of range, return the default value.

        - **Params**
            - `data`: `List`, ``
            - `index`: `int`, ``
            - `default`: `Optional[Any]`, ``

        - **Returns**
            - `Union[Dict[str, Any], None]`: ``


    - `slice_list`
        - **Description**: Return a slice of the list between start and end indexes.
If end is None, return the rest of the list.

        - **Params**
            - `data`: `List`, ``
            - `start`: `int`, ``
            - `end`: `Optional[int]`, ``

        - **Returns**
            - `List[Dict[str, Any]]`: ``


    - `strip_params`
        - **Description**: Strip None values from a group of kwargs.
And return a dictionary of the remaining values.
This is useful for filtering out None values from the parameters passed to AWS API calls.


        - **Returns**
            - `Dict[str, Any]`: ``


    - `search_metadata`
        - **Description**: Use jmespath to query the data.
This is useful for filtering out data from the AWS API response.

        - **Params**
            - `data`: `Union[Dict[str, Any], List[Dict[str, Any]]]`, ``
            - `expression`: `str`, ``

        - **Returns**
            - `Union[Dict[str, Any], List[Dict[str, Any]]]`: ``



---

- **Static Methods**
    - None

---

- **Class Methods**
    - None
