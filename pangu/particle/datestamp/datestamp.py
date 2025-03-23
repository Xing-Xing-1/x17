#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime, timedelta  # type: ignore
from typing import Dict, Literal, Optional, Union

import pytz  # type: ignore
from pangu.particle.constant.timezone import TIMEZONE_TABLE
from pangu.particle.constant.timezone import DEFUALT_TIME_ZONE
from pangu.particle.constant.timezone import DEFUALT_TIME_ZONE_NAME
from pangu.particle.duration import Duration  # type: ignore


class Datestamp:
    TIME_ZONE_NAME = DEFUALT_TIME_ZONE_NAME
    TIME_ZONE = DEFUALT_TIME_ZONE
    DATE_FORMAT = "%Y-%m-%d"
    TIME_FORMAT = "%H:%M:%S"
    DATE_TIME_FORMAT = f"{DATE_FORMAT} {TIME_FORMAT}"
    
    # --- attribute methods ---
    
    @classmethod
    def set(
        cls, 
        date_format: str = None,
        time_format: str = None,
        date_time_format: str = None,
        time_zone_name: str = None,
    ) -> None:
        """
        Set class variables
        :param date_format (str): Date format
        :param time_format (str): Time format
        :param date_time_format (str): Datetime format
        :param time_zone_name (pytz.timezone): Timezone
        :return: None
        
        """
        if date_format: cls.DATE_FORMAT = date_format
        if time_format: cls.TIME_FORMAT = time_format
        if date_time_format: cls.DATE_TIME_FORMAT = date_time_format
        if time_zone_name:
            cls.TIME_ZONE_NAME = time_zone_name
            cls.TIME_ZONE = pytz.timezone(time_zone_name)
    
    @classmethod
    def get_time_zone(cls) -> pytz.timezone:
        return cls.TIME_ZONE
    
    @classmethod
    def get_time_zone_name(self) -> str:
        return self.TIME_ZONE_NAME
    
    @classmethod
    def get_date_format(cls) -> str:
        return cls.DATE_FORMAT
    
    @classmethod
    def get_time_format(cls) -> str:
        return cls.TIME_FORMAT
    
    @classmethod
    def get_date_time_format(cls) -> str:
        return cls.DATE_TIME_FORMAT
    
    # --- create methods ---
    
    @classmethod
    def now(
        cls, 
        time_zone_name:str = None,
    ) -> "Datestamp":
        """
        Get current datestamp
        returns: Datestamp: Current date and time
        
        """
        dt = datetime.now(
            pytz.timezone(time_zone_name or cls.TIME_ZONE_NAME),
        )
        return cls(
            year=dt.year,
            month=dt.month,
            day=dt.day,
            hour=dt.hour,
            minute=dt.minute,
            second=dt.second,
            microsecond=dt.microsecond,
            time_zone_name=time_zone_name or cls.TIME_ZONE_NAME,
        )
    
    @classmethod
    def from_datetime(
        cls, 
        dt: datetime, 
        time_zone_name:str = None,
    ) -> "Datestamp":
        """
        Create datestamp object from datetime
        returns: datestamp object
        
        """
        return cls(
            year=dt.year,
            month=dt.month,
            day=dt.day,
            hour=dt.hour,
            minute=dt.minute,
            second=dt.second,
            microsecond=dt.microsecond,
            time_zone_name=time_zone_name or cls.TIME_ZONE_NAME,
        )
    
    @classmethod
    def from_timestamp(
        cls,
        timestamp: float,
        time_zone_name:str = None,
    ) -> "Datestamp":
        """
        Create Datestamp from timestamp
        returns: Datestamp: Datestamp object
        
        """
        tz = pytz.timezone(time_zone_name or cls.TIME_ZONE_NAME)
        dt = datetime.fromtimestamp(timestamp, tz)
        return cls(
            year=dt.year,
            month=dt.month,
            day=dt.day,
            hour=dt.hour,
            minute=dt.minute,
            second=dt.second,
            microsecond=dt.microsecond,
            time_zone_name=time_zone_name or cls.TIME_ZONE_NAME,
        )
    
    @classmethod
    def from_string(
        cls, 
        string, 
        date_time_format = None,
        time_zone_name:str = None,
    ) -> "Datestamp":
        """
        Create Datestamp from string
        returns: Datestamp: Datestamp object
        
        """
        tz = pytz.timezone(time_zone_name or cls.TIME_ZONE_NAME)
        dt_format = date_time_format or cls.DATE_TIME_FORMAT
        dt = datetime.strptime(string, dt_format,)
        return cls(
            year=dt.year,
            month=dt.month,
            day=dt.day,
            hour=dt.hour,
            minute=dt.minute,
            second=dt.second,
            microsecond=dt.microsecond,
            time_zone_name=time_zone_name or cls.TIME_ZONE_NAME,
        )
    
    @classmethod
    def from_dict(
        cls,
        dictionary: Dict[str, Union[int, str]],
    ) -> "Datestamp":
        """
        Create Datestamp from dictionary
        returns: Datestamp: Datestamp object
        
        """
        return cls(
            year=dictionary.get("year"),
            month=dictionary.get("month"),
            day=dictionary.get("day"),
            hour=dictionary.get("hour"),
            minute=dictionary.get("minute"),
            second=dictionary.get("second"),
            microsecond=dictionary.get("microsecond"),
            time_zone_name=dictionary.get("time_zone_name") or cls.TIME_ZONE_NAME,
        )
    
    
    def __init__(
        self,
        year: Optional[int] = None,
        month: Optional[int] = None,
        day: Optional[int] = None,
        hour: Optional[int] = 0,
        minute: Optional[int] = 0,
        second: Optional[int] = 0,
        microsecond: Optional[int] = 0,
        time_zone_name: Optional[str] = None,
    ):
        """
        Initialize Datestamp with date and time components.
        Args:
            year (int): Year
            month (int): Month
            day (int): Day
            hour (int): Hour
            minute (int): Minute
            second (int): Second
            microsecond (int): Microsecond
            tzinfo (pytz.timezone): Timezone info
            
        """
        if year is None or month is None or day is None:
            raise ValueError("year, month, and day must be provided")
        
        self.time_zone_name = time_zone_name or DEFUALT_TIME_ZONE_NAME
        self.time_zone = pytz.timezone(self.time_zone_name)
        
        # --- Step 3: Default to now() if everything is None ---
        if all(v is None for v in [year, month, day]):
            self.datetime = datetime.now(self.time_zone)
        else:
            self.datetime = datetime(
                year=year,
                month=month,
                day=day,
                hour=hour or 0,
                minute=minute or 0,
                second=second or 0,
                microsecond=microsecond or 0,
                tzinfo=self.time_zone,
            )
        
        self.year = self.datetime.year
        self.month = self.datetime.month
        self.day = self.datetime.day
        self.hour = self.datetime.hour
        self.minute = self.datetime.minute
        self.second = self.datetime.second
        self.microsecond = self.datetime.microsecond
    
    @property
    def attr(self) -> list:
        return ["year", "month", "day", "hour", "minute", "second", "microsecond", "time_zone_name"]
    
    @property
    def dict(self) -> Dict[str, Union[int, str]]:
        return {
            "year": self.year,
            "month": self.month,
            "day": self.day,
            "hour": self.hour,
            "minute": self.minute,
            "second": self.second,
            "microsecond": self.microsecond,
            "time_zone_name": self.time_zone_name,
        }
    
    def __repr__(self):
        attr_parts = []
        for key in self.attr:
            value = getattr(self, key, None)
            attr_parts.append(f"{key}={repr(value)}")
        return f"Datestamp({', '.join(attr_parts)})"

    def __str__(self):
        return self.datetime.strftime(self.DATE_TIME_FORMAT)