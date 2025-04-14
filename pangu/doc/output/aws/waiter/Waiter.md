- **Documentation**
    - **Name**: `Waiter`
    - **Path**: `aws/waiter/waiter.py`
    - **Module**: `aws/waiter`
    - **Type**
        - **Functionalities**: `[]`
        - **Structures**: `[]`
        - **Roles**: `[]`
    - **Parent**
        - **Parents**: `[]`
    - **Ref**
        - **Refs**: `['jmespath', 'math', 'pangu.particle.log.log_stream', 'time', 'typing']`
    - **Desc**
        - `A class to wait for a condition to be met by repeatedly calling a getter function.
The condition is defined by a JMESPath expression and a set of expected values.
The class supports inversion of the condition, custom interval and number of attempts.
note that compare mode has to be one of ['==', '!=', 'in', 'not in', 'exists', 'not exists'].

This class provides a flexible, extensible, and service-agnostic way to wait for changes
in AWS resource state, or any other asynchronous backend operation. Instead of relying on
boto3 built-in waiters—which are limited in scope, poorly documented, and hard to customize—
this implementation offers a unified interface that can operate on any JSON-like API response.

The condition is evaluated via a JMESPath expression (`get_path`) and compared against a set of
expected values using various compare modes. Inversion is supported to wait for non-existence or
negated conditions (e.g., wait until a resource is deleted). This class also supports configurable
timeouts and polling intervals, and integrates with the platform's logging system for observability.

This class is essential when building generalized AWS service clients, where standardized polling
behavior is required across services like EC2, S3, Redshift, VPC, and beyond.`
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
    - `getter`
        - **Type**: `Callable[..., Dict]`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `get_path`
        - **Type**: `str`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `expected`
        - **Type**: `Union[Any, List[Any]]`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `params`
        - **Type**: `Optional[Dict[str, Any]]`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `description`
        - **Type**: `Optional[str]`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `interval`
        - **Type**: `int`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `attempts`
        - **Type**: `int`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `timeout`
        - **Type**: `Optional[int]`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `invert`
        - **Type**: `bool`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `compare_mode`
        - **Type**: `str`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `log_stream`
        - **Type**: `Optional[LogStream]`
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
            - `getter`: `Callable[..., Dict]`, ``
            - `get_path`: `str`, ``
            - `expected`: `Union[Any, List[Any]]`, ``
            - `params`: `Optional[Dict[str, Any]]`, ``
            - `description`: `Optional[str]`, ``
            - `interval`: `int`, ``
            - `attempts`: `int`, ``
            - `timeout`: `Optional[int]`, ``
            - `invert`: `bool`, ``
            - `compare_mode`: `str`, ``
            - `log_stream`: `Optional[LogStream]`, ``



    - `dict`


        - **Returns**
            - `Dict[str, Any]`: ``


    - `__str__`




    - `__repr__`




    - `wait`
        - **Description**: Run the waiter until the expected condition is met or timeout occurs.

        - **Params**
            - `check`: `Any`, ``

        - **Returns**
            - `bool`: ``


    - `evaluate`
        - **Description**: Evaluate the actual value against the expected values based on the compare mode.

        - **Params**
            - `actual`: `Any`, ``

        - **Returns**
            - `bool`: ``



---

- **Static Methods**
    - None

---

- **Class Methods**
    - None
