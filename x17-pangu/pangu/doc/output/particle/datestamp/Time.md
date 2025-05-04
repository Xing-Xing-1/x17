- **Documentation**
    - **Name**: `Time`
    - **Path**: `particle/datestamp/time.py`
    - **Module**: `particle/datestamp`
    - **Type**
        - **Functionalities**: `[]`
        - **Structures**: `[]`
        - **Roles**: `[]`
    - **Parent**
        - **Parents**: `['Datestamp']`
    - **Ref**
        - **Refs**: `['datetime', 'pangu.particle.datestamp.datestamp', 'pangu.particle.duration.duration', 'pytz', 'typing']`
    - **Desc**
        - `A subclass of Datestamp that only represents a time (hour, minute, second).
Date attributes are disabled, and adding/subtracting durations returns Time.`
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
    - `hour`
        - **Type**: `Any`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `minute`
        - **Type**: `Any`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `second`
        - **Type**: `Any`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `microsecond`
        - **Type**: `Any`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `time_zone_name`
        - **Type**: `Any`
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
            - `hour`: `Any`, ``
            - `minute`: `Any`, ``
            - `second`: `Any`, ``
            - `microsecond`: `Any`, ``
            - `time_zone_name`: `Any`, ``



    - `attr`


        - **Returns**
            - `list`: ``


    - `__add__`

        - **Params**
            - `other`: `Any`, ``



    - `__sub__`

        - **Params**
            - `other`: `Any`, ``



    - `__repr__`




    - `__dir__`




    - `to_datestamp`

        - **Params**
            - `year`: `Any`, ``
            - `month`: `Any`, ``
            - `day`: `Any`, ``
            - `time_zone_name`: `Any`, ``

        - **Returns**
            - `Datestamp`: ``


    - `export`
        - **Description**: Export datestamp object as a dictionary
:return: dict: Dictionary representation of the datestamp


        - **Returns**
            - `Dict[str, Union[int, float]]`: ``



---

- **Static Methods**
    - None

---

- **Class Methods**
    - `now`
        
        - **Params**
            - `time_zone_name`: `Any`, ``

        - **Returns**
            - `'Time'`: `Time`

    - `from_string`
        
        - **Params**
            - `string`: `str`, ``
            - `time_format`: `str`, ``
            - `time_zone_name`: `str`, ``

        - **Returns**
            - `'Time'`: `Time`

    - `from_timestamp`
        
        - **Params**
            - `timestamp`: `float`, ``
            - `time_zone_name`: `str`, ``

        - **Returns**
            - `'Time'`: `Time`

