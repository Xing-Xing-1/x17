#!/usr/bin/python
# -*- coding: utf-8 -*-

from moto.particle.duration import duration  # type: ignore
from moto.particle.constant import (  # type: ignore
    TIMEZONE_TABLE,
)
from datetime import (  # type: ignore
    datetime,
    timedelta,
)
import pytz  # type: ignore


class datestamp:
    DEFAULT_TIME_ZONE = "Australia/Sydney"
    TIME_ZONE = pytz.timezone(DEFAULT_TIME_ZONE)
    DATE_FORMAT = "%Y-%m-%d"
    TIME_FORMAT = "%H:%M:%S"
    DATESTAMP_FORMAT = "%Y-%m-%d %H:%M:%S"

    @classmethod
    def show_time_zones(cls):
        return TIMEZONE_TABLE

    @classmethod
    def set_timezone(cls, time_zone):
        cls.TIME_ZONE = time_zone

    @classmethod
    def set_time_format(cls, time_format):
        cls.TIME_FORMAT = time_format

    @classmethod
    def set_date_format(cls, date_format):
        cls.DATE_FORMAT = date_format

    @classmethod
    def set_datestamp_format(cls, datestamp_format):
        cls.DATESTAMP_FORMAT = datestamp_format

    @classmethod
    def from_str(
        cls,
        datestamp_str,
        date_format=None,
        time_format=None,
        datestamp_format=None,
        time_zone=None,
    ):
        datestamp_object = cls()
        datestamp_object.set(
            datetime_obj=datetime.strptime(
                datestamp_str,
                datestamp_format or cls.DATESTAMP_FORMAT,
            ),
            date_format=date_format,
            time_format=time_format,
            datestamp_format=datestamp_format,
            time_zone=time_zone,
        )
        return datestamp_object

    @classmethod
    def from_timestamp(
        cls,
        timestamp,
        date_format=None,
        time_format=None,
        datestamp_format=None,
        time_zone=None,
    ):
        datestamp_object = cls()
        datestamp_object.set(
            datetime_obj=datetime.fromtimestamp(timestamp, time_zone or cls.TIME_ZONE),
            date_format=date_format,
            time_format=time_format,
            datestamp_format=datestamp_format,
            time_zone=time_zone,
        )
        return datestamp_object

    # Init method
    def __init__(
        self,
        datetime_obj=None,
        date_format=None,
        time_format=None,
        datestamp_format=None,
        time_zone=None,
    ):
        self.time_zone = time_zone if time_zone else self.TIME_ZONE
        self.date_format = date_format or self.DATE_FORMAT
        self.time_format = time_format or self.TIME_FORMAT
        self.datestamp_format = datestamp_format or self.DATESTAMP_FORMAT

        self.datestamp = datetime_obj or datetime.now()
        self.datestamp = self.datestamp.replace(tzinfo=self.time_zone)
        self.date = self.datestamp.date()
        self.time = self.datestamp.time()

    def set(
        self,
        datetime_obj=None,
        date_format=None,
        time_format=None,
        datestamp_format=None,
        time_zone=None,
    ):
        self.__init__(
            datetime_obj=datetime_obj,
            date_format=date_format,
            time_format=time_format,
            datestamp_format=datestamp_format,
            time_zone=time_zone,
        )

    def __str__(self):
        return self.get_datestamp_str()

    def __dict__(self):
        return {
            "datestamp": self.get_datestamp_str(),
            "time_zone": self.get_time_zone(),
        }

    def get_date_str(self):
        return self.date.strftime(self.date_format)

    def get_time_str(self):
        return self.time.strftime(self.time_format)

    def get_datestamp_str(self):
        return self.datestamp.strftime(self.datestamp_format)

    def get_timestamp(self):
        return int(self.datestamp.timestamp())

    def get_time_zone(self):
        return self.time_zone

    def get_date(self):
        return self.date

    def get_time(self):
        return self.time

    def get_datestamp(self):
        return self.datestamp

    """
		Operations

	"""

    def subtract_datestamp(self, datestamp_obj):
        if not isinstance(datestamp_obj, datestamp):
            raise Exception("datestamp_obj must be an instance of datestamp class")
        return duration(
            round((self.datestamp - datestamp_obj.get_datestamp()).total_seconds()),
            "second",
        )

    def diff(self, datestamp_obj, absolute=False):
        if not isinstance(datestamp_obj, datestamp):
            raise Exception("datestamp_obj must be an instance of datestamp class")
        if absolute:
            return abs(self.subtract_datestamp(datestamp_obj))
        else:
            return self.subtract_datestamp(datestamp_obj)

    def __sub__(self, duration_obj):
        return datestamp(
            self.datestamp - timedelta(seconds=duration_obj.to_second()),
            self.date_format,
            self.time_format,
            self.datestamp_format,
            self.time_zone,
        )

    def add_duration(self, duration_obj):
        if not isinstance(duration_obj, duration):
            raise Exception("duration_obj must be an instance of duration class")
        return datestamp(
            self.datestamp + timedelta(seconds=duration_obj.to_second()),
            self.date_format,
            self.time_format,
            self.datestamp_format,
            self.time_zone,
        )

    def __add__(self, duration_obj):
        return self.add_duration(duration_obj)

    def __ne__(self, value: object):
        return not self.__eq__(value)

    def __eq__(self, value: object):
        if not isinstance(value, datestamp):
            return False
        return self.get_datestamp() == value.get_datestamp()

    def __lt__(self, value: object):
        if not isinstance(value, datestamp):
            return False
        return self.get_datestamp() < value.get_datestamp()

    def __le__(self, value: object):
        if not isinstance(value, datestamp):
            return False
        return self.get_datestamp() <= value.get_datestamp()

    def __gt__(self, value: object):
        if not isinstance(value, datestamp):
            return False
        return self.get_datestamp() > value.get_datestamp()

    def __ge__(self, value: object):
        if not isinstance(value, datestamp):
            return False
        return self.get_datestamp() >= value.get_datestamp()
