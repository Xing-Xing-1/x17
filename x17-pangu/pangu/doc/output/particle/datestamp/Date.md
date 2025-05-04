- **Documentation**
    - **Name**: `Date`
    - **Path**: `particle/datestamp/date.py`
    - **Module**: `particle/datestamp`
    - **Type**
        - **Functionalities**: `[]`
        - **Structures**: `[]`
        - **Roles**: `[]`
    - **Parent**
        - **Parents**: `['Datestamp']`
    - **Ref**
        - **Refs**: `['datetime', 'pangu.particle.datestamp.datestamp', 'pangu.particle.datestamp.time', 'pangu.particle.duration.duration', 'pytz', 'typing']`
    - **Desc**
        - `A subclass of Datestamp that only represents a date (year, month, day).
Time attributes are disabled, and adding/subtracting durations returns Date.`
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
    - `year`
        - **Type**: `Any`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `month`
        - **Type**: `Any`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `day`
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
            - `year`: `Any`, ``
            - `month`: `Any`, ``
            - `day`: `Any`, ``
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



    - `combine`

        - **Params**
            - `time`: `'Time'`, ``

        - **Returns**
            - `Datestamp`: ``


    - `__repr__`




    - `__dir__`




    - `to_datestamp`

        - **Params**
            - `hour`: `Any`, ``
            - `minute`: `Any`, ``
            - `second`: `Any`, ``
            - `microsecond`: `Any`, ``
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
    - `today`
        
        - **Params**
            - `time_zone_name`: `Any`, ``

        - **Returns**
            - `'Date'`: `Date`

    - `from_string`
        
        - **Params**
            - `string`: `str`, ``
            - `date_format`: `str`, ``
            - `time_zone_name`: `str`, ``

        - **Returns**
            - `'Date'`: `Date`

    - `from_timestamp`
        
        - **Params**
            - `timestamp`: `float`, ``
            - `time_zone_name`: `str`, ``

        - **Returns**
            - `'Date'`: `Date`

