- **Documentation**
    - **Name**: `Ec2Client`
    - **Path**: `aws/ec2/client.py`
    - **Module**: `aws/ec2`
    - **Type**
        - **Functionalities**: `[]`
        - **Structures**: `[]`
        - **Roles**: `[]`
    - **Parent**
        - **Parents**: `['AwsClient']`
    - **Ref**
        - **Refs**: `['boto3', 'pangu.aws.base.aws_client', 'pangu.aws.session', 'pangu.aws.waiter', 'pangu.particle.log.log_group', 'pangu.particle.log.log_stream', 'time', 'typing']`
    - **Desc**
        - `Inherit from the base class AwsClient.
Provides a common interface for AWS EC2 clients.
Including platform behaviors including logging and plugin registration.`
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



    - `list_vpcs`
        - **Description**: List all VPC configurations in the current region/account.

        - **Params**
            - `filters`: `Optional[List[Dict[str, Any]]]`, ``
            - `vpc_ids`: `Optional[List[str]]`, ``
            - `max_results`: `Optional[int]`, ``
            - `dry_run`: `Optional[bool]`, ``

        - **Returns**
            - `List[Dict[str, Any]]`: ``


    - `get_default_vpc`
        - **Description**: Get the default VPC for the current region/account.

        - **Params**
            - `dry_run`: `bool`, ``

        - **Returns**
            - `Optional[Dict[str, Any]]`: ``


    - `get_vpc`
        - **Description**: Get the VPC configuration by VPC ID.

        - **Params**
            - `vpc_id`: `str`, ``
            - `dry_run`: `bool`, ``

        - **Returns**
            - `Optional[Dict[str, Any]]`: ``


    - `create_security_group`
        - **Description**: Create a new security group.
If exists_ok is False, raise an exception.
If exists_ok is True, return the existing group id.

        - **Params**
            - `group_name`: `str`, ``
            - `description`: `str`, ``
            - `vpc_id`: `Optional[str]`, ``
            - `tag_specifications`: `Optional[List[Dict[str, Any]]]`, ``
            - `dry_run`: `Optional[bool]`, ``
            - `wait`: `Optional[bool]`, ``
            - `exists_ok`: `Optional[bool]`, ``

        - **Returns**
            - `Dict[str, Any]`: ``


    - `wait_create_security_group`
        - **Description**: Wait until the security group (by ID and VPC) is created.

        - **Params**
            - `group_id`: `str`, ``
            - `vpc_id`: `str`, ``
            - `timeout`: `Optional[int]`, ``
            - `interval`: `Optional[int]`, ``

        - **Returns**
            - `bool`: ``


    - `get_security_group`
        - **Description**: Possible values for filters:
group-id: The security group ID.
description: The security groups description.
group-name: The security group name.
owner-id: The security group owner ID.
primary-vpc-id: The VPC ID in which the security group was created.

        - **Params**
            - `vpc_id`: `str`, ``
            - `max_results`: `Optional[int]`, ``
            - `filters`: `Optional[List[Dict[str, Any]]]`, ``
            - `dry_run`: `Optional[bool]`, ``



    - `get_security_group_by_id`

        - **Params**
            - `group_id`: `str`, ``
            - `vpc_id`: `str`, ``
            - `max_results`: `Optional[int]`, ``
            - `dry_run`: `Optional[bool]`, ``



    - `get_security_group_by_name`
        - **Description**: Get the security group by name.

        - **Params**
            - `group_name`: `str`, ``
            - `vpc_id`: `str`, ``
            - `max_results`: `Optional[int]`, ``
            - `dry_run`: `Optional[bool]`, ``



    - `exists_security_group_by_name`
        - **Description**: Check if the security group exists by name.

        - **Params**
            - `group_name`: `str`, ``
            - `vpc_id`: `str`, ``



    - `list_security_groups`
        - **Description**: List all security groups in the current region/account.
Possible values for filters:
group-id: The security group ID.
group-name: The security group name.
owner-id: The security group owner ID.
primary-vpc-id: The VPC ID in which the security group was created.

        - **Params**
            - `group_ids`: `Optional[list]`, ``
            - `group_names`: `Optional[list]`, ``
            - `max_results`: `Optional[int]`, ``
            - `dry_run`: `Optional[bool]`, ``
            - `filters`: `Optional[Dict[str, Union[str, list]]]`, ``

        - **Returns**
            - `List[Dict[str, Any]]`: ``


    - `list_security_group_by_vpc`
        - **Description**: List all security groups in the VPC.

        - **Params**
            - `vpc_id`: `str`, ``
            - `max_results`: `Optional[int]`, ``
            - `dry_run`: `Optional[bool]`, ``

        - **Returns**
            - `List[Dict[str, Any]]`: ``


    - `delete_security_group`
        - **Description**: Delete the security group by ID or name.

        - **Params**
            - `group_id`: `str`, ``
            - `group_name`: `Optional[str]`, ``
            - `dry_run`: `Optional[bool]`, ``
            - `wait`: `Optional[bool]`, ``



    - `wait_delete_security_group`
        - **Description**: Wait until the security group is deleted.

        - **Params**
            - `group_id`: `str`, ``
            - `timeout`: `Optional[int]`, ``
            - `interval`: `Optional[int]`, ``

        - **Returns**
            - `bool`: ``


    - `authorize_security_group_ingress`

        - **Params**
            - `cidr_ip`: `str`, ``
            - `from_port`: `int`, ``
            - `group_id`: `str`, ``
            - `group_name`: `Optional[str]`, ``
            - `ip_permisions`: `Optional[Dict[str, Any]]`, ``
            - `ip_protocol`: `Optional[str]`, ``
            - `source_security_group_name`: `Optional[str]`, ``
            - `source_security_group_owner_id`: `Optional[str]`, ``
            - `to_port`: `int`, ``
            - `tag_specifications`: `Optional[List[Dict[str, Any]]]`, ``
            - `dry_run`: `Optional[bool]`, ``

        - **Returns**
            - `Dict[str, Any]`: ``


    - `authorise_ingress_from_cidr_ips`

        - **Params**
            - `group_id`: `str`, ``
            - `cidr_ips_configs`: `List[Dict[str, Any]]`, ``



    - `authorise_ingress_from_security_groups`

        - **Params**
            - `group_id`: `str`, ``
            - `security_groups_configs`: `List[Dict[str, Any]]`, ``



    - `authorise_ingress_from_self`

        - **Params**
            - `group_id`: `str`, ``
            - `security_groups_configs`: `List[Dict[str, Any]]`, ``




---

- **Static Methods**
    - None

---

- **Class Methods**
    - None
