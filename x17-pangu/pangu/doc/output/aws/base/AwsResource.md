- **Documentation**
    - **Name**: `AwsResource`
    - **Path**: `aws/base/aws_resource.py`
    - **Module**: `aws/base`
    - **Type**
        - **Functionalities**: `[]`
        - **Structures**: `[]`
        - **Roles**: `[]`
    - **Parent**
        - **Parents**: `[]`
    - **Ref**
        - **Refs**: `['pangu.aws.base.aws_client', 'pangu.particle.log.log_group', 'pangu.particle.log.log_stream', 'pangu.particle.text.id', 'typing']`
    - **Desc**
        - `Base class for AWS resources.
This class provides a common interface for AWS resources, including logging and plugin registration.
Normally set the log module to log stream.`
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
    - `resource_id`
        - **Type**: `Optional[str]`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `account_id`
        - **Type**: `Optional[str]`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `region`
        - **Type**: `Optional[str]`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `raw`
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
    - None

---

- **Instance Methods**
    - `__init__`

        - **Params**
            - `resource_id`: `Optional[str]`, ``
            - `account_id`: `Optional[str]`, ``
            - `region`: `Optional[str]`, ``
            - `raw`: `Optional[Dict[str, Any]]`, ``
            - `log_group`: `Optional[LogGroup]`, ``



    - `__str__`




    - `__repr__`




    - `log`
        - **Description**: Log a message to the log stream.
This method allows logging messages at different levels (e.g., INFO, ERROR).
Normally assign the log level to the log stream.

Args:
    message (str): _description_
    level (str, optional): _description_. Defaults to "INFO".

        - **Params**
            - `message`: `str`, ``
            - `level`: `str`, ``



    - `register_plugin`
        - **Description**: Register a plugin to the resource.
Plugin could be any object (AwsResource, AwsClient, etc.)
This method allows adding custom functionality to the resource.

Args:
    name (str): The name of the plugin.
    plugin (Any): The plugin to register.
Returns:
    Tuple[str, Any]: The name and plugin.

        - **Params**
            - `name`: `str`, ``
            - `plugin`: `Any`, ``



    - `dict`
        - **Description**: Convert the resource to a dictionary representation.

Returns:
    Dict[str, Any]: _description_


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
            - `resource_id`: `str`, ``
            - `account_id`: `Optional[str]`, ``
            - `region`: `Optional[str]`, ``
            - `log_group`: `Optional[LogGroup]`, ``


