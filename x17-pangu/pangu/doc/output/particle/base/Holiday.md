- **Documentation**
    - **Name**: `Holiday`
    - **Path**: `particle/base/holiday.py`
    - **Module**: `particle/base`
    - **Type**
        - **Functionalities**: `[]`
        - **Structures**: `[]`
        - **Roles**: `[]`
    - **Parent**
        - **Parents**: `[]`
    - **Ref**
        - **Refs**: `['datetime', 'holidays', 'pangu.particle.datestamp']`
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
    - `country_code`
        - **Type**: `Any`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `subdiv`
        - **Type**: `Any`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `year`
        - **Type**: `Any`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`

---

- **Attributes**
    - `DEFAULT_COUNTRY`
        - **Type**: `Any`
        - **Desc**: ``
    - `DEFAULT_SUBDIV`
        - **Type**: `Any`
        - **Desc**: ``

---

- **Instance Methods**
    - `__init__`

        - **Params**
            - `country_code`: `Any`, ``
            - `subdiv`: `Any`, ``
            - `year`: `Any`, ``



    - `__str__`




    - `__dict__`




    - `is_holiday`

        - **Params**
            - `datestamp`: `Datestamp`, ``

        - **Returns**
            - `bool`: ``


    - `list_holidays`




    - `list_holiday_dates`

        - **Params**
            - `as_datestamp`: `Any`, ``



    - `list_holiday_names`




    - `export`

        - **Params**
            - `as_datestamp`: `Any`, ``




---

- **Static Methods**
    - None

---

- **Class Methods**
    - `au_nsw`
        
        - **Params**
            - `year`: `Any`, ``


    - `au`
        
        - **Params**
            - `year`: `Any`, ``


    - `set_default_country`
        
        - **Params**
            - `country_code`: `Any`, ``


    - `set_default_subdiv`
        
        - **Params**
            - `subdiv`: `Any`, ``


