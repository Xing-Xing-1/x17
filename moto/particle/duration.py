#!/usr/bin/python
# -*- coding: utf-8 -*-

from moto.particle.constant import (  # type: ignore
    TIME_UNIT_TABLE,
)


class duration:
    def __init__(self, duration, unit="second"):
        self.duration = duration
        self.unit = unit

    def __str__(self):
        return f"{self.duration} {self.unit}"

    def __dict__(self):
        return {
            "duration": self.duration,
            "unit": self.unit,
        }

    def get_duration(self):
        return self.duration

    def get_unit(self):
        return self.unit

    def round_to(self, number, round_to=0):
        return round(number, round_to)

    def to_unit(self, unit="second", round_to=None):
        if not unit or unit == "second":
            return self.to_second(round_to)
        elif unit == "minute":
            return self.to_minute(round_to)
        elif unit == "hour":
            return self.to_hour(round_to)
        elif unit == "day":
            return self.to_day(round_to)
        elif unit == "week":
            return self.to_week(round_to)
        elif unit == "month":
            return self.to_month(round_to)
        elif unit == "year":
            return self.to_year(round_to)
        else:
            raise Exception(
                "unit must be one of the following: second, minute, hour, day, week, month, year"
            )

    def to_second(self, round_to=None):
        result = self.duration * TIME_UNIT_TABLE[self.unit]
        return self.round_to(result, round_to) if round_to is not None else result

    def to_minute(self, round_to=None):
        result = self.duration * TIME_UNIT_TABLE[self.unit] / TIME_UNIT_TABLE["minute"]
        return self.round_to(result, round_to) if round_to is not None else result

    def to_hour(self, round_to=None):
        result = self.duration * TIME_UNIT_TABLE[self.unit] / TIME_UNIT_TABLE["hour"]
        return self.round_to(result, round_to) if round_to is not None else result

    def to_day(self, round_to=None):
        result = self.duration * TIME_UNIT_TABLE[self.unit] / TIME_UNIT_TABLE["day"]
        return self.round_to(result, round_to) if round_to is not None else result

    def to_week(self, round_to=None):
        result = self.duration * TIME_UNIT_TABLE[self.unit] / TIME_UNIT_TABLE["week"]
        return self.round_to(result, round_to) if round_to is not None else result

    def to_month(self, round_to=None):
        result = self.duration * TIME_UNIT_TABLE[self.unit] / TIME_UNIT_TABLE["month"]
        return self.round_to(result, round_to) if round_to is not None else result

    def to_year(self, round_to=None):
        result = self.duration * TIME_UNIT_TABLE[self.unit] / TIME_UNIT_TABLE["year"]
        return self.round_to(result, round_to) if round_to is not None else result

    def as_unit(self, unit="second", round_to=None):
        if not unit or unit == "second":
            return self.as_second(round_to)
        elif unit == "minute":
            return self.as_minute(round_to)
        elif unit == "hour":
            return self.as_hour(round_to)
        elif unit == "day":
            return self.as_day(round_to)
        elif unit == "week":
            return self.as_week(round_to)
        elif unit == "month":
            return self.as_month(round_to)
        elif unit == "year":
            return self.as_year(round_to)
        else:
            raise Exception(
                "unit must be one of the following: second, minute, hour, day, week, month, year"
            )

    def as_second(self, round_to=None):
        self.__init__(self.to_second(round_to), "second")

    def as_minute(self, round_to=None):
        self.__init__(self.to_minute(round_to), "minute")

    def as_hour(self, round_to=None):
        self.__init__(self.to_hour(round_to), "hour")

    def as_day(self, round_to=None):
        self.__init__(self.to_day(round_to), "day")

    def as_week(self, round_to=None):
        self.__init__(self.to_week(round_to), "week")

    def as_month(self, round_to=None):
        self.__init__(self.to_month(round_to), "month")

    def as_year(self, round_to=None):
        self.__init__(self.to_year(round_to), "year")

    """
		Operations

	"""

    def __abs__(self):
        return duration(abs(self.duration), self.unit)

    def __add__(self, duration_obj, unit=None):
        if not isinstance(duration_obj, duration):
            raise Exception("other must be an instance of duration class")

        result_duration = duration(
            self.to_second() + duration_obj.to_second(), "second"
        )
        result_duration.as_unit(unit)
        return result_duration

    def __sub__(self, duration_obj):
        if not isinstance(duration_obj, duration):
            raise Exception("other must be an instance of duration class")

        sub_duration = self.to_second() - duration_obj.to_second()
        result_duration = duration(sub_duration, "second")
        result_duration.as_unit(duration_obj.unit)
        return result_duration

    def __mul__(self, number):
        return duration(self.duration * number, self.unit)
