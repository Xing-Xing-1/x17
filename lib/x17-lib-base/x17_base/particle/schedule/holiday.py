# -*- coding: utf-8 -*-
from typing import Any, Dict, Optional
from datetime import date, datetime
import holidays

from x17_base.particle.datestamp import Datestamp


class Holiday:
    DEFAULT_COUNTRY = "AU"
    DEFAULT_SUBDIV = None

    @classmethod
    def set_default_country(cls, country_code):
        cls.DEFAULT_COUNTRY = country_code

    @classmethod
    def set_default_subdiv(cls, subdiv):
        cls.DEFAULT_SUBDIV = subdiv

    @classmethod
    def au_nsw(cls, year=None):
        if year is None:
            year = Datestamp.now().year
        return cls(
            country_code="AU",
            subdiv="NSW",
            year=year,
        )

    @classmethod
    def au(cls, year=None):
        if year is None:
            year = Datestamp.now().year
        return cls(
            country_code="AU",
            year=year,
        )
        
    @classmethod
    def cn(cls, year=None):
        if year is None:
            year = Datestamp.now().year
        return cls(
            country_code="CN",
            year=year,
        )

    def __init__(
        self,
        country_code="AU",
        subdiv=None,
        year=None,
    ):
        self.country_code = country_code or self.DEFAULT_COUNTRY
        self.subdiv = subdiv or self.DEFAULT_SUBDIV
        self.year = year or Datestamp.now().year
        params = {
            "subdiv": self.subdiv,
            "years": self.year,
        }
        params = {k: v for k, v in params.items() if v is not None}
        self.holidays = holidays.country_holidays(
            self.country_code,
            **params,
        )

    @property
    def attr(self) -> list[str]:
        return ["country_code", "subdiv", "year"]
        
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
        return f"{self.country_code} {self.subdiv} {self.year}"

    def is_holiday(self, datestamp: Datestamp) -> bool:
        return datestamp.datetime.date() in self.holidays

    def list_raw_holidays(self):
        return sorted(self.holidays.items())
    
    def list_holidays(self, as_datestamp=False):
        result = []
        for holiday_dt, holiday_name in self.list_raw_holidays():
            dt = Datestamp.from_datetime(
                datetime.combine(holiday_dt, datetime.min.time()),
            ) if as_datestamp else holiday_dt
            result.append((dt, holiday_name,))
        return result
        
    def list_holiday_dates(self, as_datestamp=False):
        return [
            Datestamp.from_datetime(
                datetime.combine(holiday_date, datetime.min.time()),
            )
            if as_datestamp else holiday_date
            for holiday_date, _ in self.list_raw_holidays()
        ]

    def list_holiday_names(self):
        return [holiday_name for _, holiday_name in self.list_raw_holidays()]

    def export(self):
        return {
            "country_code": self.country_code,
            "subdiv": self.subdiv,
            "year": self.year,
            "holidays": self.list_holidays(),
        }