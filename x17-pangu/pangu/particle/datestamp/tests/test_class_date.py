#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime
import pytz
import pytest

from pangu.particle.datestamp.date import Date
from pangu.particle.datestamp.time import Time
from pangu.particle.duration import Duration


def test_init_and_repr():
    d = Date(2025, 3, 24)
    assert d.year == 2025
    assert d.month == 3
    assert d.day == 24
    assert "Date(year=2025" in repr(d)


def test_today():
    today = Date.today()
    assert isinstance(today, Date)


def test_add_duration():
    d = Date(2025, 3, 24)
    result = d + Duration(day=3)
    assert isinstance(result, Date)
    assert result.day == 27


def test_sub_duration():
    d = Date(2025, 3, 24)
    result = d - Duration(day=4)
    assert result.day == 20


def test_sub_date():
    d1 = Date(2025, 3, 30)
    d2 = Date(2025, 3, 25)
    diff = d1 - d2
    assert isinstance(diff, Duration)
    assert diff.day == 5


def test_invalid_add():
    d = Date(2025, 3, 24)
    with pytest.raises(TypeError):
        _ = d + 123


def test_combine_with_time():
    d = Date(2025, 3, 24)
    t = Time(14, 30)
    combined = d.combine(t)
    assert combined.year == 2025
    assert combined.hour == 14


def test_from_string_default_format():
    d = Date.from_string("2025-03-28")
    assert d.year == 2025
    assert d.month == 3
    assert d.day == 28


def test_from_string_custom_format():
    d = Date.from_string("28/03/2025", "%d/%m/%Y")
    assert d.month == 3


def test_from_timestamp():
    ts = datetime(2025, 3, 28, 14, 30, tzinfo=pytz.UTC).timestamp()
    d = Date.from_timestamp(ts, time_zone_name="UTC")
    assert d.year == 2025
    assert d.day == 28


def test_time_to_datestamp_full():
    t = Time(14, 30)
    dt = t.to_datestamp(year=2025, month=3, day=28)
    assert dt.year == 2025
    assert dt.hour == 14


def test_time_to_datestamp_partial():
    t = Time(9, 15)
    dt = t.to_datestamp(day=5)
    assert dt.day == 5
    assert dt.hour == 9


def test_time_to_datestamp_with_timezone():
    t = Time(10, 0, time_zone_name="Asia/Tokyo")
    dt = t.to_datestamp(year=2025, month=4, day=1, time_zone_name="UTC")
    assert dt.time_zone.zone == "UTC"


def test_date_to_datestamp_full():
    d = Date(2025, 3, 28)
    dt = d.to_datestamp(hour=14, minute=30, second=15, microsecond=100000)
    assert dt.hour == 14
    assert dt.microsecond == 100000


def test_date_to_datestamp_with_timezone():
    d = Date(2025, 3, 28, time_zone_name="Asia/Shanghai")
    dt = d.to_datestamp(time_zone_name="UTC")
    assert dt.time_zone.zone == "UTC"


def test_export():
    d = Date(2025, 3, 28)
    exported = d.export()
    assert exported["year"] == 2025
    assert exported["month"] == 3
    assert exported["day"] == 28
    assert "time_zone_name" in exported
    
    