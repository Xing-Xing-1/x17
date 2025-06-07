# test_class_holiday.py

import pytest
from datetime import datetime, date
from x17_base.particle.datestamp import Datestamp
from x17_base.particle.schedule.holiday import Holiday


def test_holiday_au_nsw_is_holiday():
    h = Holiday.au_nsw(2025)
    ds = Datestamp.from_datetime(datetime(2025, 1, 1), time_zone_name="Australia/Sydney")
    assert h.is_holiday(ds) is True


def test_holiday_au_export_and_list_methods():
    h = Holiday.au_nsw(2025)
    as_ds = h.export()

    assert isinstance(as_ds, dict)
    assert "country_code" in as_ds
    assert "subdiv" in as_ds
    assert "year" in as_ds
    print(as_ds)
    assert all(isinstance(k, tuple) for k in as_ds.get("holidays"))
    assert all(isinstance(v.__class__.__name__, str) for v in as_ds.values())

    names = h.list_holiday_names()
    dates = h.list_holiday_dates()
    dates_as_ds = h.list_holiday_dates(as_datestamp=True)
    
    assert all(isinstance(name, str) for name in names)
    assert all(isinstance(d, date) for d in dates)
    assert all(isinstance(d, Datestamp) for d in dates_as_ds)


def test_holiday_repr_and_dict():
    h = Holiday(country_code="AU", subdiv="NSW", year=2025)
    d = h.dict

    assert isinstance(repr(h), str)
    assert isinstance(d, dict)
    assert d["country_code"] == "AU"
    assert d["subdiv"] == "NSW"
    assert d["year"] == 2025


def test_holiday_str_output():
    h = Holiday(country_code="AU", subdiv="NSW", year=2025)
    assert str(h) == "AU NSW 2025"


def test_holiday_cn_safe_instantiation():
    h = Holiday.cn(2025)
    assert isinstance(h, Holiday)
    
    