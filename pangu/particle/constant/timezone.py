#!/usr/bin/python
# -*- coding: utf-8 -*-

from datetime import datetime
import pytz # type: ignore


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

class ConstantTimezone:
    def __init__(self):
        self.TIMEZONE_TABLE = {
            timezone: int(
                pytz.timezone(timezone).utcoffset(datetime.now()).total_seconds() / 3600
            )
            for timezone in pytz.all_timezones
        }