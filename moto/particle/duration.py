#!/usr/bin/python
# -*- coding: utf-8 -*-

from moto.particle.constant import ( # type: ignore
	TIME_UNIT_TABLE,
)

class duration():
	def __init__(self, duration, unit = "second"):
		self.duration = duration
		self.unit = unit
		
	def __str__(self):
		return f"{self.duration} {self.unit}"
	
	def __dict__(self):
		return {
			"duration": self.duration,
			"unit": self.unit,
		}

	def round_to(self, number, round_to = 0):
		return round(number, round_to)

	def to_second(self, round_to = None):
		result = self.duration * TIME_UNIT_TABLE[self.unit] 
		return self.round_to(result, round_to) if round_to is not None else result 
	
	def to_minute(self, round_to = None):
		result = self.duration * TIME_UNIT_TABLE[self.unit] / TIME_UNIT_TABLE["minute"]
		return self.round_to(result, round_to) if round_to is not None else result
	
	def to_hour(self, round_to = None):
		result = self.duration * TIME_UNIT_TABLE[self.unit] / TIME_UNIT_TABLE["hour"]
		return self.round_to(result, round_to) if round_to is not None else result
	
	def to_day(self, round_to = None):
		result = self.duration * TIME_UNIT_TABLE[self.unit] / TIME_UNIT_TABLE["day"]
		return self.round_to(result, round_to) if round_to is not None else result
	
	def to_week(self, round_to = None):
		result = self.duration * TIME_UNIT_TABLE[self.unit] / TIME_UNIT_TABLE["week"]
		return self.round_to(result, round_to) if round_to is not None else result
	
	def to_month(self, round_to = None):
		result = self.duration * TIME_UNIT_TABLE[self.unit] / TIME_UNIT_TABLE["month"]
		return self.round_to(result, round_to) if round_to is not None else result
	
	def to_year(self, round_to = None):
		result = self.duration * TIME_UNIT_TABLE[self.unit] / TIME_UNIT_TABLE["year"]
		return self.round_to(result, round_to) if round_to is not None else result
	
	def as_second(self, round_to = None):
		return self.__init__(self.to_second(round_to), "second")
	
	def as_minute(self, round_to = None):
		return self.__init__(self.to_minute(round_to), "minute")
	
	def as_hour(self, round_to = None):
		return self.__init__(self.to_hour(round_to), "hour")
	
	def as_day(self, round_to = None):
		return self.__init__(self.to_day(round_to), "day")
	
	def as_week(self, round_to = None):
		return self.__init__(self.to_week(round_to), "week")
	
	def as_month(self, round_to = None):
		return self.__init__(self.to_month(round_to), "month")
	
	def as_year(self, round_to = None):
		return self.__init__(self.to_year(round_to), "year")
	
	def get_duration(self):
		return self.duration
	
	def get_unit(self):
		return self.unit