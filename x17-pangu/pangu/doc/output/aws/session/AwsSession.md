- **Documentation**
    - **Name**: `AwsSession`
    - **Path**: `aws/session/session.py`
    - **Module**: `aws/session`
    - **Type**
        - **Functionalities**: `[]`
        - **Structures**: `[]`
        - **Roles**: `[]`
    - **Parent**
        - **Parents**: `[]`
    - **Ref**
        - **Refs**: `['boto3', 'pangu.particle.log.log_group', 'pangu.particle.log.log_stream', 'typing']`
    - **Desc**
        - `AWS Session class.
This class provides a common interface for AWS sessions.
Including logging and plugin registration.
Can either support Ec2 instance runtime or local runtime.
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
    - `access_key`
        - **Type**: `Any`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `secret_key`
        - **Type**: `Any`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `session_token`
        - **Type**: `Any`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `botocore_session`
        - **Type**: `Any`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `aws_account_id`
        - **Type**: `Any`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `profile_name`
        - **Type**: `Any`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `region_name`
        - **Type**: `Any`
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
            - `access_key`: `Any`, ``
            - `secret_key`: `Any`, ``
            - `session_token`: `Any`, ``
            - `botocore_session`: `Any`, ``
            - `aws_account_id`: `Any`, ``
            - `profile_name`: `Any`, ``
            - `region_name`: `Any`, ``
            - `log_group`: `Optional[LogGroup]`, ``



    - `client`
        - **Description**: Create a boto3 client for the given service.
This is a wrapper for the boto3 session client method.

        - **Params**
            - `service_name`: `str`, ``
            - `region_name`: `Optional[str]`, ``
            - `aws_account_id`: `Optional[str]`, ``
            - `aws_access_key_id`: `Optional[str]`, ``
            - `aws_secret_access_key`: `Optional[str]`, ``
            - `aws_session_token`: `Optional[str]`, ``
            - `api_version`: `Optional[str]`, ``
            - `use_ssl`: `Optional[bool]`, ``
            - `verify`: `Optional[bool]`, ``
            - `endpoint_url`: `Optional[str]`, ``
            - `config`: `Optional[Dict[str, Any]]`, ``



    - `list_regions`
        - **Description**: List all available regions for a given service and partition.

        - **Params**
            - `service_name`: `Optional[str]`, ``
            - `partition_name`: `Optional[str]`, ``

        - **Returns**
            - `list`: ``


    - `list_partitions`
        - **Description**: List all available partitions.


        - **Returns**
            - `list`: ``


    - `list_services`
        - **Description**: List all available services.


        - **Returns**
            - `list`: ``


    - `get_credentials`
        - **Description**: Get the credentials for the session.
This is a wrapper for the boto3 session get_credentials method.
The credentials are returned as a dictionary.





---

- **Static Methods**
    - None

---

- **Class Methods**
    - None
