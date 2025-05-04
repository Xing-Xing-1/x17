- **Documentation**
    - **Name**: `StsClient`
    - **Path**: `aws/sts/client.py`
    - **Module**: `aws/sts`
    - **Type**
        - **Functionalities**: `[]`
        - **Structures**: `[]`
        - **Roles**: `[]`
    - **Parent**
        - **Parents**: `['AwsClient']`
    - **Ref**
        - **Refs**: `['boto3', 'pangu.aws.base.aws_client', 'pangu.aws.session', 'pangu.particle.duration', 'pangu.particle.log.log_group', 'pangu.particle.log.log_stream', 'typing']`
    - **Desc**
        - `AWS STS (Security Token Service) client.
This class provides a common interface for interacting with STS, including logging, account info caching,
and assuming roles. It extends the AwsClient base class for unified AWS logging and utilities.`
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
    - `region`
        - **Type**: `Optional[str]`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `session`
        - **Type**: `Optional[AwsSession]`
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
            - `account_id`: `Optional[str]`, ``
            - `region`: `Optional[str]`, ``
            - `session`: `Optional[AwsSession]`, ``



    - `_load`
        - **Description**: Load account information from STS.
This method caches the account ID, user ARN, and user ID for later use.




    - `describe_caller`
        - **Description**: Describe the caller identity.
This method retrieves the account ID, user ARN, and user ID from STS.


        - **Returns**
            - `Dict[str, str]`: ``


    - `get_account_id`
        - **Description**: Get the account ID.


        - **Returns**
            - `Optional[str]`: ``


    - `get_region`
        - **Description**: Get the region.


        - **Returns**
            - `Optional[str]`: ``


    - `get_user_arn`
        - **Description**: Get the user ARN.


        - **Returns**
            - `Optional[str]`: ``


    - `get_user_id`
        - **Description**: Get the user ID.


        - **Returns**
            - `Optional[str]`: ``


    - `get_cred_from_assume_role`
        - **Description**: Get temporary credentials by assuming a role.

        - **Params**
            - `role_arn`: `str`, ``
            - `role_session_name`: `str`, ``
            - `duration`: `Duration`, ``

        - **Returns**
            - `dict`: ``



---

- **Static Methods**
    - None

---

- **Class Methods**
    - None
