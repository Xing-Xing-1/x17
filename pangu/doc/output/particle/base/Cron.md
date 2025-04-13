- **Documentation**
    - **Name**: `Cron`
    - **Path**: `particle/base/cron.py`
    - **Module**: `particle/base`
    - **Type**
        - **Functionalities**: `[]`
        - **Structures**: `[]`
        - **Roles**: `[]`
    - **Parent**
        - **Parents**: `[]`
    - **Ref**
        - **Refs**: `['datetime', 'pangu.particle.datestamp', 'pyawscron', 'pytz']`
    - **Desc**
        - `In lib pyawscron
All time-related operations are done in UTC
Manually convert to the desired timezone if needed.`
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
    - `cron_str`
        - **Type**: `str`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`

---

- **Attributes**
    - `DEFAULT_TIME_ZONE_NAME`
        - **Type**: `Any`
        - **Desc**: ``

---

- **Instance Methods**
    - `__init__`

        - **Params**
            - `cron_str`: `str`, ``



    - `__str__`




    - `__repr__`




    - `__eq__`

        - **Params**
            - `other`: `Any`, ``



    - `__ne__`

        - **Params**
            - `other`: `Any`, ``



    - `__dict__`




    - `get_schedules_between`

        - **Params**
            - `start`: `Datestamp`, ``
            - `end`: `Datestamp`, ``
            - `time_zone_name`: `str`, ``



    - `get_schedules_next`

        - **Params**
            - `start`: `Datestamp`, ``
            - `time_zone_name`: `str`, ``
            - `count`: `int`, ``



    - `get_schedules_prev`

        - **Params**
            - `start`: `Datestamp`, ``
            - `time_zone_name`: `str`, ``
            - `count`: `int`, ``




---

- **Static Methods**
    - None

---

- **Class Methods**
    - `validate`
        
        - **Params**
            - `cron_str`: `str`, ``

        - **Returns**
            - `bool`: ``

