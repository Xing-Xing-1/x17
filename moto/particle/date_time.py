#!/usr/bin/python
# -*- coding: utf-8 -*-

from x17.moto.particle.duration import duration # type: ignore
from x17.moto.particle.constant import ( # type: ignore
	TIMEZONE_TABLE,
)
from datetime import ( # type: ignore
	datetime,
	timedelta,
)
import pytz # type: ignore


class date_time():
	DEFAULT_TIME_ZONE = "Australia/Sydney"
	TIME_ZONE = pytz.timezone(DEFAULT_TIME_ZONE)
	DATE_FORMAT = "%Y-%m-%d"
	TIME_FORMAT = "%H:%M:%S"
	DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

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
	def set_date_time_format(cls, date_time_format):
		cls.DATE_TIME_FORMAT = date_time_format
	
	@classmethod
	def from_str(
			cls,
			date_time_str,
			date_format = None, 
			time_format = None,
			date_time_format = None,
			time_zone = None,
		):
		date_time_object = cls()
		date_time_object.set(
			datetime_obj = datetime.strptime(
				date_time_str, 
				date_time_format or cls.DATE_TIME_FORMAT,
			),
			date_format = date_format,
			time_format = time_format,
			date_time_format = date_time_format,
			time_zone = time_zone,
		)
		return date_time_object

	@classmethod
	def from_timestamp(
			cls,
			timestamp,
			date_format = None, 
			time_format = None,
			date_time_format = None,
			time_zone = None,
		):
		date_time_object = cls()
		date_time_object.set(
			datetime_obj = datetime.fromtimestamp(
				timestamp,
				time_zone or cls.TIME_ZONE
			),
			date_format = date_format,
			time_format = time_format,
			date_time_format = date_time_format,
			time_zone = time_zone,
		)
		return date_time_object

	# Init method 
	def __init__(
			self, 
			datetime_obj = None,
			date_format = None, 
			time_format = None,
			date_time_format = None,
			time_zone = None,
		):
			self.time_zone = time_zone if time_zone else self.TIME_ZONE
			self.date_format = date_format or self.DATE_FORMAT
			self.time_format = time_format or self.TIME_FORMAT
			self.date_time_format = date_time_format or self.DATE_TIME_FORMAT

			self.date_time = datetime_obj or datetime.now()
			self.date_time = self.date_time.replace(tzinfo=self.time_zone)
			self.date = self.date_time.date()
			self.time = self.date_time.time()
    
	def set(
			self,
			datetime_obj = None,
			date_format = None, 
			time_format = None,
			date_time_format = None,
			time_zone = None,
		):
		self.__init__(
			datetime_obj = datetime_obj,
			date_format = date_format,
			time_format = time_format,
			date_time_format = date_time_format,
			time_zone = time_zone,
		)
	
	def __str__(self):
		return self.get_date_time_str()
	
	def __dict__(self):
		return {
			"date_time": self.get_date_time_str(),
			"time_zone": self.get_time_zone(),
		}
	
	def get_date_str(self):
		return self.date.strftime(self.date_format)

	def get_time_str(self):
		return self.time.strftime(self.time_format)
	
	def get_date_time_str(self):
		return self.date_time.strftime(self.date_time_format)
	
	def get_timestamp(self):
		return int(self.date_time.timestamp())
	
	def get_time_zone(self):
		return self.time_zone
	
	def get_date(self):
		return self.date
	
	def get_time(self):
		return self.time
	
	def get_date_time(self):
		return self.date_time
	
	def diff(self, date_time_obj, abs = False, unit = "second"):
		if not isinstance(date_time_obj, date_time):
			raise ValueError("date_time object type expected, got {}".format(type(date_time_obj)))
		
		if unit not in duration.TIME_UNIT_TABLE:
			raise ValueError("invalid duration unit = {}".format(duration.TIME_UNIT_TABLE.keys()))

		diff = self.date_time - date_time_obj.get_date_time()
		diff = abs(diff.total_seconds()) if abs else diff.total_seconds()

		
		