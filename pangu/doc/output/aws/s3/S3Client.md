- **Documentation**
    - **Name**: `S3Client`
    - **Path**: `aws/s3/client.py`
    - **Module**: `aws/s3`
    - **Type**
        - **Functionalities**: `[]`
        - **Structures**: `[]`
        - **Roles**: `[]`
    - **Parent**
        - **Parents**: `['AwsClient']`
    - **Ref**
        - **Refs**: `['boto3', 'botocore.exceptions', 'json', 'pangu.aws.base.aws_client', 'pangu.aws.session', 'pangu.particle.log.log_group', 'pangu.particle.log.log_stream', 're', 'typing']`
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
    - `max_paginate`
        - **Type**: `Optional[int]`
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
            - `service`: `Optional[str]`, ``
            - `region`: `Optional[str]`, ``
            - `plugin`: `Optional[Dict[str, Any]]`, ``
            - `log_group`: `Optional[LogGroup]`, ``
            - `max_paginate`: `Optional[int]`, ``
            - `session`: `Optional[AwsSession]`, ``



    - `parse_uri`
        - **Description**: Parses the S3 URI and returns the bucket name and prefix.
The URI format is expected to be "s3://bucket-name/prefix" or "bucket-name/prefix".

        - **Params**
            - `uri`: `str`, ``

        - **Returns**
            - `tuple[str, str]`: ``


    - `list_objects`
        - **Description**: Lists all files in the bucket with the given suffix.
Optionally filtering by key prefix and file suffix.
Suffix suggestion = [0-9a-zA-Z]+

        - **Params**
            - `uri`: `str`, ``
            - `suffix`: `Optional[str]`, ``
            - `prefix`: `Optional[str]`, ``



    - `check_exist`
        - **Description**: Check if the object exists at the given S3 URI.

        - **Params**
            - `uri`: `str`, ``

        - **Returns**
            - `bool`: ``


    - `get_object`
        - **Description**: Get an S3 object.

        - **Params**
            - `bucket`: `str`, ``
            - `key`: `str`, ``

        - **Returns**
            - `dict`: ``


    - `delete_object`
        - **Description**: Delete an S3 object.

        - **Params**
            - `bucket`: `str`, ``
            - `key`: `str`, ``



    - `put_object`
        - **Description**: Upload object to S3.

        - **Params**
            - `bucket`: `str`, ``
            - `key`: `str`, ``
            - `data`: `Union[str, bytes]`, ``



    - `put_json_object`
        - **Description**: Put a Python dict as JSON to S3.

        - **Params**
            - `bucket`: `str`, ``
            - `key`: `str`, ``
            - `data`: `Optional[dict]`, ``



    - `get_json_object`
        - **Description**: Get an S3 object and parse it as JSON.

        - **Params**
            - `bucket`: `str`, ``
            - `key`: `str`, ``

        - **Returns**
            - `dict`: ``


    - `get_txt_object`
        - **Description**: Get an S3 object and parse it as text.

        - **Params**
            - `bucket`: `str`, ``
            - `key`: `str`, ``

        - **Returns**
            - `str`: ``


    - `put_txt_object`
        - **Description**: Put a string as text to S3.

        - **Params**
            - `bucket`: `str`, ``
            - `key`: `str`, ``
            - `data`: `str`, ``




---

- **Static Methods**
    - `bucket_of`
        - **Description**: Extracts the bucket name from the S3 URI.

        - **Returns**
            - `str | None`: ``

    - `prefix_of`
        - **Description**: Extracts the prefix from the S3 URI.

        - **Returns**
            - `str | None`: ``


---

- **Class Methods**
    - None
