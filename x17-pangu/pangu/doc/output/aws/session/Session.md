- **Documentation**
    - **Name**: `Session`
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
        - `PARAMETERS:
    access_key (string): AWS access key ID
    secret_key (string): AWS secret access key
    token (string): AWS temporary session token
    region_name (string): Default region when creating new connections
    botocore_session (botocore.session.Session): Use this Botocore session instead of creating a new default one.
    profile_name (string): The name of a profile to use. If not given, then the default profile is used.
    aws_account_id (string): AWS account ID
    `
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



    - `list_regions`

        - **Params**
            - `service_name`: `Optional[str]`, ``
            - `partition_name`: `Optional[str]`, ``

        - **Returns**
            - `list`: ``


    - `list_partitions`


        - **Returns**
            - `list`: ``


    - `list_services`


        - **Returns**
            - `list`: ``


    - `get_credentials`





---

- **Static Methods**
    - None

---

- **Class Methods**
    - None
