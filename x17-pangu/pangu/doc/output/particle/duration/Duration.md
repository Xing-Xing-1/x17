- **Documentation**
    - **Name**: `Duration`
    - **Path**: `particle/duration/duration.py`
    - **Module**: `particle/duration`
    - **Type**
        - **Functionalities**: `[]`
        - **Structures**: `[]`
        - **Roles**: `[]`
    - **Parent**
        - **Parents**: `[]`
    - **Ref**
        - **Refs**: `['datetime', 'dateutil.relativedelta', 'pangu.particle.constant.time', 'time', 'typing']`
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
    - `week`
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
    - `millisecond`
        - **Type**: `Optional[int]`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `microsecond`
        - **Type**: `Optional[int]`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `nanosecond`
        - **Type**: `Optional[int]`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `normalize`
        - **Type**: `bool`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`
    - `normalize_mode`
        - **Type**: `Literal['calendar', 'strict', 'flat']`
        - **Desc**: ``
        - **Optional**: `False`
        - **Default**: `None`

---

- **Attributes**
    - `TIME_UNIT_TABLE`
        - **Type**: `Any`
        - **Desc**: ``
    - `TIME_UNIT_TABLE_INDEX`
        - **Type**: `Any`
        - **Desc**: ``
    - `TIME_UNITS`
        - **Type**: `Any`
        - **Desc**: ``

---

- **Instance Methods**
    - `__init__`
        - **Description**: 初始化 Duration 对象，支持指定单位的数值或具体的时间参数。
:param value: 数值

:attr base: 对象的总秒数

        - **Params**
            - `year`: `Optional[int]`, ``
            - `month`: `Optional[int]`, ``
            - `week`: `Optional[int]`, ``
            - `day`: `Optional[int]`, ``
            - `hour`: `Optional[int]`, ``
            - `minute`: `Optional[int]`, ``
            - `second`: `Optional[int]`, ``
            - `millisecond`: `Optional[int]`, ``
            - `microsecond`: `Optional[int]`, ``
            - `nanosecond`: `Optional[int]`, ``
            - `normalize`: `bool`, ``
            - `normalize_mode`: `Literal['calendar', 'strict', 'flat']`, ``

        - **Returns**
            - `None`: `None`


    - `attr`


        - **Returns**
            - `list`: ``


    - `dict`


        - **Returns**
            - `Dict[str, int]`: ``


    - `base`
        - **Description**: 作为基础单位（秒）的属性
:return: Duration 对象的总秒数


        - **Returns**
            - `Union[int, float]`: ``


    - `get_base`
        - **Description**: 返回所有单位转换为基础单位（秒）的总和。
:return: Duration 对象的总秒数


        - **Returns**
            - `Union[int, float]`: ``


    - `as_normalize`


        - **Returns**
            - `None`: `None`


    - `__repr__`


        - **Returns**
            - `str`: ``


    - `__str__`


        - **Returns**
            - `str`: ``


    - `__add__`

        - **Params**
            - `other`: `Union['Duration', timedelta, relativedelta]`, ``

        - **Returns**
            - `'Duration'`: `Duration`


    - `__sub__`

        - **Params**
            - `other`: `Union['Duration', timedelta, relativedelta]`, ``

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


    - `__radd__`

        - **Params**
            - `other`: `Union['Duration', timedelta, relativedelta]`, ``

        - **Returns**
            - `'Duration'`: `Duration`


    - `__mul__`

        - **Params**
            - `factor`: `Union[int, float]`, ``

        - **Returns**
            - `'Duration'`: `Duration`


    - `__truediv__`

        - **Params**
            - `divisor`: `Union[int, float]`, ``

        - **Returns**
            - `'Duration'`: `Duration`


    - `__hash__`


        - **Returns**
            - `int`: ``


    - `__bool__`


        - **Returns**
            - `bool`: ``


    - `describe`
        - **Description**: 返回 Duration 对象的描述（人类可读）
例如: "1 year, 2 months, 3 days"

:return: 描述字符串

        - **Params**
            - `as_text`: `Any`, ``

        - **Returns**
            - `str`: ``


    - `set`
        - **Description**: 设置 Duration 对象的属性
:param kwargs: 属性字典
    - year: int
    - month: int
    - week: int
    - day: int
    - hour: int
    - minute: int
    - second: int
    - millisecond: int
    - microsecond: int


        - **Returns**
            - `None`: `None`


    - `export`


        - **Returns**
            - `Dict[str, Union[int, float, str]]`: ``


    - `wait`
        - **Description**: 等待指定的时间段
:return: None


        - **Returns**
            - `None`: `None`



---

- **Static Methods**
    - None

---

- **Class Methods**
    - `set_precise`
        - **Description**: 设置 Duration 为精确模式
考虑到闰年和月份的天数差异，精确模式下的时间单位表如下：
- year: 365.25 days
- month: 30.4375 days

:return: None
        

        - **Returns**
            - `None`: `None`

    - `from_dict`
        - **Description**: 从字典创建 Duration 实例。
:param dictionary: 包含时间单位的字典
    - year: int
    - month: int
    - week: int
    - day: int
    - hour: int
    - minute: int
    - second: int
    - millisecond: int
    - microsecond: int
:return: Duration 实例
        
        - **Params**
            - `dictionary`: `Dict[str, int]`, ``

        - **Returns**
            - `'Duration'`: `Duration`

    - `from_timedelta`
        - **Description**: 从 datetime.timedelta 创建 Duration 实例.
注意: timedelta 不包含 year 或 month 信息.
:param td: datetime.timedelta 对象
:param normalise: 是否归一化

:return: Duration 实例
        
        - **Params**
            - `td`: `timedelta`, ``
            - `normalise`: `bool`, ``

        - **Returns**
            - `'Duration'`: `Duration`

    - `from_relativedelta`
        - **Description**: 从 dateutil.relativedelta 创建 Duration 实例.
注意: relativedelta 不包含 week 信息.
:param rd: dateutil.relativedelta 对象
:param normalise: 是否归一化

:return: Duration 实例
        
        - **Params**
            - `rd`: `relativedelta`, ``
            - `normalise`: `bool`, ``

        - **Returns**
            - `'Duration'`: `Duration`

