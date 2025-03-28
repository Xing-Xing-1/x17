from datetime import datetime, timedelta
import pytz
from pangu.particle.datestamp import Datestamp
from pangu.particle.duration import Duration
from pangu.particle.datestamp.time import Time

class Date(Datestamp):
    """
    A subclass of Datestamp that only represents a date (year, month, day).
    Time attributes are disabled, and adding/subtracting durations returns Date.
    
    """

    @classmethod
    def today(cls, time_zone_name=None) -> "Date":
        tz = pytz.timezone(time_zone_name or cls.TIME_ZONE_NAME)
        now = datetime.now(tz)
        return cls(now.year, now.month, now.day, time_zone_name)
    
    def __init__(self, year, month, day, time_zone_name=None):
        super().__init__(year, month, day, 0, 0, 0, 0, time_zone_name)

    def __add__(self, other):
        if isinstance(other, Duration):
            new_dt = self.datetime + timedelta(seconds=other.base)
            return Date(new_dt.year, new_dt.month, new_dt.day, self.time_zone_name)
        raise TypeError("Date can only be added with Duration")

    def __sub__(self, other):
        if isinstance(other, Duration):
            new_dt = self.datetime - timedelta(seconds=other.base)
            return Date(new_dt.year, new_dt.month, new_dt.day, self.time_zone_name)
        elif isinstance(other, Date):
            delta = self.datetime - other.datetime
            return Duration.from_timedelta(delta)
        raise TypeError("Date can only be subtracted with Duration or another Date")

    def combine(self, time: "Time") -> Datestamp:
        return Datestamp(
            year=self.year,
            month=self.month,
            day=self.day,
            hour=time.hour,
            minute=time.minute,
            second=time.second,
            microsecond=time.microsecond,
            time_zone_name=self.time_zone_name,
        )

    def __repr__(self):
        attr_parts = []
        for key in self.attr:
            value = getattr(self, key, None)
            attr_parts.append(f"{key}={repr(value)}")
        return f"Date({', '.join(attr_parts)})"

    def __dir__(self):
        base = super().__dir__()
        return [item for item in base if item not in {"hour", "minute", "second", "microsecond"}]

