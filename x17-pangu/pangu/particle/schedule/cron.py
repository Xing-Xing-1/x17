from pyawscron import AWSCron
from typing import Any, Dict, Optional
from datetime import datetime as py_native_dt
from datetime import timezone as py_native_tz
import pytz

from pangu.particle.datestamp import Datestamp


class Cron:
    """
    In lib pyawscron time-related operations are in UTC
    Manually convert to the desired timezone if needed
    
    """
    DEFAULT_TIME_ZONE_NAME = "UTC"
    
    @classmethod
    def from_str(
        cls, 
        expression: str,
        time_zone_name: Optional[str] = None,
    ) -> "Cron":
        return cls(
            expression=expression,
            time_zone_name=time_zone_name,
        )

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Cron":
        expression = data.get("expression")
        time_zone_name = data.get("time_zone_name")
        return cls(
            expression=expression,
            time_zone_name=time_zone_name,
        )
        
    @classmethod
    def validate(cls, cron: str) -> bool:
        try:
            _ = AWSCron(cron)
            return True
        except Exception:
            return False

    def __init__(
        self, 
        expression: str,
        time_zone_name: Optional[str] = None,
    ):
        self.expression = expression
        self.cron = AWSCron(self.expression)
        self.minutes = self.cron.minutes
        self.hours = self.cron.hours
        self.days_of_month = self.cron.days_of_month
        self.months = self.cron.months
        self.days_of_week = self.cron.days_of_week
        self.years = self.cron.years
        self.time_zone_name = time_zone_name or self.DEFAULT_TIME_ZONE_NAME
        self.time_zone = pytz.timezone(self.time_zone_name)

    @property
    def attr(self) -> list[str]:
        return [
            key
            for key in self.__dict__.keys()
            if not key.startswith("_") and isinstance(self.__dict__[key], str)
        ]

    @property
    def dict(self) -> Dict[str, str]:
        return {key: getattr(self, key) for key in self.attr}

    def __repr__(self):
        attr_parts = []
        for key in self.attr:
            value = getattr(self, key, None)
            attr_parts.append(f"{key}={repr(value)}")
        return f"{self.__class__.__name__}({', '.join(attr_parts)})"

    def __str__(self):
        return self.expression

    def __eq__(self, other):
        return isinstance(other, Cron) and self.expression == other.expression

    def __ne__(self, other):
        return not self.__eq__(other)

    def get_schedules_between(
        self,
        start: Datestamp,
        end: Datestamp,
    ):
        start_utc = start.to_timezone("UTC")
        end_utc = end.to_timezone("UTC")
        results = AWSCron.get_all_schedule_bw_dates(
            py_native_dt.strptime(
                start_utc.datestamp_str, 
                Datestamp.DATE_TIME_FORMAT,
            ).replace(tzinfo=py_native_tz.utc),
            py_native_dt.strptime(
                end_utc.datestamp_str, 
                Datestamp.DATE_TIME_FORMAT,
            ).replace(tzinfo=py_native_tz.utc),
            self.expression,
        )
        return [
            Datestamp.from_datetime(
                dt, 
                time_zone_name="UTC",
            ).to_timezone(
                self.time_zone_name,
            )
            for dt in results
        ]

    def get_schedules_next(
        self,
        start: Datestamp = None,
        count: int = 1,
    ):
        count = 100 if count > 100 else count
        start = Datestamp.now(self.time_zone_name) if start is None else start
        start_utc = start.to_timezone("UTC")
        results = AWSCron.get_next_n_schedule(
            count,
            py_native_dt.strptime(
                start_utc.datestamp_str,
                Datestamp.DATE_TIME_FORMAT,
            ).replace(
                tzinfo=py_native_tz.utc,
            ),
            self.expression,
        )
        return [
            Datestamp.from_datetime(
                dt, 
                time_zone_name="UTC",
            ).to_timezone(
                self.time_zone_name,
            )
            for dt in results
        ]

    def get_schedules_prev(
        self,
        start: Datestamp = None,
        count: int = 1,
    ):
        count = 100 if count > 100 else count
        start = Datestamp.now(self.time_zone_name) if start is None else start
        start_utc = start.to_timezone("UTC")
        results = AWSCron.get_prev_n_schedule(
            count,
            py_native_dt.strptime(
                start_utc.datestamp_str, 
                Datestamp.DATE_TIME_FORMAT,
            ).replace(
                tzinfo=py_native_tz.utc,
            ),
            self.expression,
        )
        return [
            Datestamp.from_datetime(
                dt, 
                time_zone_name="UTC",
            ).to_timezone(
                self.time_zone_name,
            )
            for dt in results
        ]

    def export(self) -> Dict[str, Any]:
        return {
            "expression": self.expression,
            "minutes": self.minutes,
            "hours": self.hours,
            "days_of_month": self.days_of_month,
            "months": self.months,
            "days_of_week": self.days_of_week,
            "years": self.years,
            "time_zone_name": self.time_zone_name,
        }
        
    