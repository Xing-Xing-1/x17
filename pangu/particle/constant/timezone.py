#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Dict, Literal, Optional, Union
import pytz  # type: ignore

"""
    Loaded all timezones from pytz and created a 
    dictionary with timezone as key and offset 
    in hours as value

"""
TIMEZONE_TABLE = {
    timezone: int(
        pytz.timezone(timezone).utcoffset(datetime.now()).total_seconds() / 3600
    )
    for timezone in pytz.all_timezones
}
DEFUALT_TIME_ZONE_NAME = "Australia/Sydney"
DEFUALT_TIME_ZONE = pytz.timezone(DEFUALT_TIME_ZONE_NAME)


class ConstantTimezone:
    def __init__(self):
        self.TIMEZONE_TABLE = {
            timezone: int(
                pytz.timezone(timezone).utcoffset(datetime.now()).total_seconds() / 3600
            )
            for timezone in pytz.all_timezones
        }

    def export(self) -> Dict[str, Union[int, float, str]]:
        return {
            key: value for key, value in self.dict.items()
            if value not in (None, "", 0, [], {}, set())
        }