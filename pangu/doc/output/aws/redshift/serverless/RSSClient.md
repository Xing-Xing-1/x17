- **Documentation**
    - **Name**: `RSSClient`
    - **Path**: `aws/redshift/serverless/client.py`
    - **Module**: `aws/redshift/serverless`
    - **Type**
        - **Functionalities**: `[]`
        - **Structures**: `[]`
        - **Roles**: `[]`
    - **Parent**
        - **Parents**: `['AwsClient']`
    - **Ref**
        - **Refs**: `['boto3', 'pangu.aws.base.aws_client', 'pangu.aws.session', 'pangu.aws.waiter', 'pangu.particle.log.log_group', 'pangu.particle.log.log_stream', 'time', 'typing']`
    - **Desc**
        - `AWS Redshift Serverless client.
This class provides a common interface for interacting with Redshift Serverless, including logging,
account info caching, and assuming roles. It extends the AwsClient base class for unified AWS logging and utilities.
It provides methods for listing, creating, updating, and deleting namespaces and workgroups.
It also provides methods for waiting for the creation and deletion of namespaces and workgroups.
The class uses the boto3 library to interact with AWS services.`
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



    - `list_namespace`
        - **Description**: List all namespaces in the account.
The namespaces are paginated, so this method will return all namespaces


        - **Returns**
            - `List[Dict[str, Any]]`: ``


    - `list_workgroup`
        - **Description**: List all workgroups in the account.
The owner account is optional and can be used to filter the workgroups by owner.

        - **Params**
            - `owner_account`: `str`, ``

        - **Returns**
            - `List[Dict[str, Any]]`: ``


    - `get_namespace`
        - **Description**: Get a namespace by name.

        - **Params**
            - `namespace_name`: `str`, ``

        - **Returns**
            - `Optional[Dict[str, Any]]`: ``


    - `get_workgroup`
        - **Description**: Get a workgroup by name.

        - **Params**
            - `workgroup_name`: `str`, ``

        - **Returns**
            - `Union[Dict[str, Any], None]`: ``


    - `create_namespace`
        - **Description**: Create a namespace with the specified parameters.

        - **Params**
            - `namespace_name`: `str`, ``
            - `admin_password_secret_kms_key_id`: `Optional[str]`, ``
            - `admin_user_password`: `Optional[str]`, ``
            - `admin_user_name`: `Optional[str]`, ``
            - `db_name`: `Optional[str]`, ``
            - `default_iam_role_arn`: `Optional[str]`, ``
            - `iam_roles`: `Optional[List[str]]`, ``
            - `kms_key_id`: `Optional[str]`, ``
            - `log_exports`: `Optional[List[str]]`, ``
            - `manage_admin_password`: `Optional[bool]`, ``
            - `redshift_idc_application_arn`: `Optional[str]`, ``
            - `tags`: `List[Dict[str, str]]`, ``
            - `wait`: `Optional[bool]`, ``

        - **Returns**
            - `Dict[str, Any]`: ``


    - `create_workgroup`
        - **Description**: Create a workgroup in the specified namespace.

        - **Params**
            - `namespace_name`: `str`, ``
            - `workgroup_name`: `str`, ``
            - `base_capacity`: `Optional[int]`, ``
            - `config_parameters`: `Optional[List[Dict[str, str]]]`, ``
            - `enhanced_vpc_routing`: `Optional[bool]`, ``
            - `max_capacity`: `Optional[int]`, ``
            - `port`: `Optional[int]`, ``
            - `price_performance_target`: `Optional[Dict[str, Union[int, str]]]`, ``
            - `publicly_accessible`: `Optional[bool]`, ``
            - `security_group_ids`: `Optional[List[str]]`, ``
            - `subnet_ids`: `Optional[List[str]]`, ``
            - `tags`: `Optional[List[Dict[str, str]]]`, ``
            - `track_name`: `Optional[str]`, ``
            - `wait`: `Optional[bool]`, ``



    - `wait_create_namespace`
        - **Description**: Wait until the namespace reaches AVAILABLE state.

        - **Params**
            - `namespace_name`: `str`, ``
            - `timeout`: `Optional[int]`, ``
            - `interval`: `Optional[int]`, ``

        - **Returns**
            - `bool`: ``


    - `wait_create_workgroup`
        - **Description**: Wait until the workgroup reaches AVAILABLE state.

        - **Params**
            - `workgroup_name`: `str`, ``
            - `timeout`: `Optional[int]`, ``
            - `interval`: `Optional[int]`, ``

        - **Returns**
            - `bool`: ``


    - `delete_workgroup`
        - **Description**: Delete a workgroup by name.
This method will delete the workgroup and all associated resources.

        - **Params**
            - `workgroup_name`: `str`, ``
            - `wait`: `Optional[bool]`, ``

        - **Returns**
            - `Dict[str, Any]`: ``


    - `delete_namespace`
        - **Description**: Delete a namespace by name.
This method will delete the namespace and all associated resources.

        - **Params**
            - `namespace_name`: `str`, ``
            - `wait`: `Optional[bool]`, ``

        - **Returns**
            - `Dict[str, Any]`: ``


    - `wait_delete_workgroup`
        - **Description**: Wait until the workgroup is deleted.

        - **Params**
            - `workgroup_name`: `str`, ``
            - `timeout`: `Optional[int]`, ``
            - `interval`: `Optional[int]`, ``

        - **Returns**
            - `bool`: ``


    - `wait_delete_namespace`
        - **Description**: Wait until the namespace is deleted.

        - **Params**
            - `namespace_name`: `str`, ``
            - `timeout`: `Optional[int]`, ``
            - `interval`: `Optional[int]`, ``

        - **Returns**
            - `bool`: ``


    - `update_namespace`
        - **Description**: Update the specified namespace with the given parameters.

        - **Params**
            - `namespace_name`: `str`, ``
            - `admin_password_secret_kms_key_id`: `Optional[str]`, ``
            - `admin_user_password`: `Optional[str]`, ``
            - `admin_user_name`: `Optional[str]`, ``
            - `default_iam_role_arn`: `Optional[str]`, ``
            - `iam_roles`: `Optional[List[str]]`, ``
            - `kms_key_id`: `Optional[str]`, ``
            - `log_exports`: `Optional[List[str]]`, ``
            - `manage_admin_password`: `Optional[bool]`, ``
            - `wait`: `Optional[bool]`, ``

        - **Returns**
            - `Dict[str, Any]`: ``


    - `update_workgroup`

        - **Params**
            - `namespace_name`: `str`, ``
            - `workgroup_name`: `str`, ``
            - `base_capacity`: `Optional[int]`, ``
            - `config_parameters`: `Optional[List[Dict[str, str]]]`, ``
            - `enhanced_vpc_routing`: `Optional[bool]`, ``
            - `max_capacity`: `Optional[int]`, ``
            - `port`: `Optional[int]`, ``
            - `price_performance_target`: `Optional[Dict[str, Union[int, str]]]`, ``
            - `publicly_accessible`: `Optional[bool]`, ``
            - `security_group_ids`: `Optional[List[str]]`, ``
            - `subnet_ids`: `Optional[List[str]]`, ``
            - `tags`: `Optional[List[Dict[str, str]]]`, ``
            - `wait`: `Optional[bool]`, ``



    - `wait_update_namespace`
        - **Description**: Wait until the namespace reaches AVAILABLE state.

        - **Params**
            - `namespace_name`: `str`, ``
            - `timeout`: `Optional[int]`, ``
            - `interval`: `Optional[int]`, ``

        - **Returns**
            - `bool`: ``


    - `wait_update_workgroup`
        - **Description**: Wait until the workgroup reaches AVAILABLE state.

        - **Params**
            - `workgroup_name`: `str`, ``
            - `timeout`: `Optional[int]`, ``
            - `interval`: `Optional[int]`, ``

        - **Returns**
            - `bool`: ``



---

- **Static Methods**
    - None

---

- **Class Methods**
    - None
