- **Documentation**
    - **Name**: `Datestamp`
    - **Path**: `particle/datestamp/datestamp.py`
    - **Module**: `particle/datestamp`
    - **Type**
        - **Functionalities**: `[]`
        - **Structures**: `[]`
        - **Roles**: `[]`
    - **Parent**
        - **Parents**: `[]`
    - **Ref**
        - **Refs**: `['datetime', 'pangu.particle.constant.timezone', 'pangu.particle.duration.duration', 'pytz', 'typing']`
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
    - `year`
        - **Type**: `Optional[int]`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `month`
        - **Type**: `Optional[int]`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `day`
        - **Type**: `Optional[int]`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `hour`
        - **Type**: `Optional[int]`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `minute`
        - **Type**: `Optional[int]`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `second`
        - **Type**: `Optional[int]`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `microsecond`
        - **Type**: `Optional[int]`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `time_zone_name`
        - **Type**: `Optional[str]`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`

---

- **Attributes**
    - `TIME_ZONE_NAME`
        - **Type**: `Any`
        - **Desc**: ``
    - `TIME_ZONE`
        - **Type**: `Any`
        - **Desc**: ``
    - `DATE_FORMAT`
        - **Type**: `Any`
        - **Desc**: ``
    - `TIME_FORMAT`
        - **Type**: `Any`
        - **Desc**: ``
    - `DATE_TIME_FORMAT`
        - **Type**: `Any`
        - **Desc**: ``

---

- **Instance Methods**
    - `__init__`
        - **Description**: Initialize Datestamp with date and time components.
Args:
    year (int): Year
    month (int): Month
    day (int): Day
    hour (int): Hour
    minute (int): Minute
    second (int): Second
    microsecond (int): Microsecond
    tzinfo (pytz.timezone): Timezone info

        - **Params**
            - `year`: `Optional[int]`, ``
            - `month`: `Optional[int]`, ``
            - `day`: `Optional[int]`, ``
            - `hour`: `Optional[int]`, ``
            - `minute`: `Optional[int]`, ``
            - `second`: `Optional[int]`, ``
            - `microsecond`: `Optional[int]`, ``
            - `time_zone_name`: `Optional[str]`, ``



    - `attr`


        - **Returns**
            - `list`: ``


    - `date_str`

        - **Params**
            - `date_format`: `str`, ``

        - **Returns**
            - `str`: ``


    - `time_str`

        - **Params**
            - `time_format`: `str`, ``

        - **Returns**
            - `str`: ``


    - `datestamp_str`

        - **Params**
            - `date_time_format`: `str`, ``

        - **Returns**
            - `str`: ``


    - `dict`


        - **Returns**
            - `Dict[str, Union[int, str]]`: ``


    - `__repr__`




    - `__str__`




    - `get_datetime`
        - **Description**: Get datetime object
returns: datetime: Datetime object


        - **Returns**
            - `datetime`: ``


    - `get_timestamp`
        - **Description**: Get timestamp
returns: float: Timestamp


        - **Returns**
            - `float`: ``


    - `set`
        - **Description**: Set attributes
:param kwargs: Attributes to set
:return: None


        - **Returns**
            - `None`: `None`


    - `__add__`

        - **Params**
            - `other`: `'Duration'`, ``

        - **Returns**
            - `'Datestamp'`: `Datestamp`


    - `__radd__`

        - **Params**
            - `other`: `'Duration'`, ``

        - **Returns**
            - `'Datestamp'`: `Datestamp`


    - `__sub__`

        - **Params**
            - `other`: `Union['Duration', 'Datestamp']`, ``

        - **Returns**
            - `Union['Datestamp', 'Duration']`: ``


    - `__rsub__`

        - **Params**
            - `other`: `'Datestamp'`, ``

        - **Returns**
            - `'Duration'`: `Duration`


    - `__eq__`

        - **Params**
            - `other`: `object`, ``

        - **Returns**
            - `bool`: ``


    - `__ne__`

        - **Params**
            - `other`: `object`, ``

        - **Returns**
            - `bool`: ``


    - `__lt__`

        - **Params**
            - `other`: `object`, ``

        - **Returns**
            - `bool`: ``


    - `__le__`

        - **Params**
            - `other`: `object`, ``

        - **Returns**
            - `bool`: ``


    - `__gt__`

        - **Params**
            - `other`: `object`, ``

        - **Returns**
            - `bool`: ``


    - `__ge__`

        - **Params**
            - `other`: `object`, ``

        - **Returns**
            - `bool`: ``


    - `__hash__`


        - **Returns**
            - `int`: ``


    - `__bool__`


        - **Returns**
            - `bool`: ``


    - `describe`
        - **Description**: Describe the datestamp
:return: str: Description

        - **Params**
            - `as_text`: `Any`, ``

        - **Returns**
            - `str`: ``


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
    - `reset`
        

        - **Returns**
            - `None`: `None`

    - `configure`
        - **Description**: Set class variables
:param date_format (str): Date format
:param time_format (str): Time format
:param date_time_format (str): Datetime format
:param time_zone_name (pytz.timezone): Timezone
:return: None
        
        - **Params**
            - `date_format`: `str`, ``
            - `time_format`: `str`, ``
            - `date_time_format`: `str`, ``
            - `time_zone_name`: `str`, ``

        - **Returns**
            - `None`: `None`

    - `get_time_zone`
        

        - **Returns**
            - `pytz.timezone`: ``

    - `get_time_zone_name`
        

        - **Returns**
            - `str`: ``

    - `get_date_format`
        

        - **Returns**
            - `str`: ``

    - `get_time_format`
        

        - **Returns**
            - `str`: ``

    - `get_date_time_format`
        

        - **Returns**
            - `str`: ``

    - `now`
        - **Description**: Get current datestamp
returns: Datestamp: Current date and time
        
        - **Params**
            - `time_zone_name`: `str`, ``

        - **Returns**
            - `'Datestamp'`: `Datestamp`

    - `from_datetime`
        - **Description**: Create datestamp object from datetime
returns: datestamp object
        
        - **Params**
            - `dt`: `datetime`, ``
            - `time_zone_name`: `str`, ``

        - **Returns**
            - `'Datestamp'`: `Datestamp`

    - `from_timestamp`
        - **Description**: Create Datestamp from timestamp
returns: Datestamp: Datestamp object
        
        - **Params**
            - `timestamp`: `float`, ``
            - `time_zone_name`: `str`, ``

        - **Returns**
            - `'Datestamp'`: `Datestamp`

    - `from_string`
        - **Description**: Create Datestamp from string
returns: Datestamp: Datestamp object
        
        - **Params**
            - `string`: `Any`, ``
            - `date_time_format`: `Any`, ``
            - `time_zone_name`: `str`, ``

        - **Returns**
            - `'Datestamp'`: `Datestamp`

    - `from_dict`
        - **Description**: Create Datestamp from dictionary
returns: Datestamp: Datestamp object
        
        - **Params**
            - `dictionary`: `Dict[str, Union[int, str]]`, ``

        - **Returns**
            - `'Datestamp'`: `Datestamp`

