#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime
import pytest
import pytz

from pangu.particle.datestamp import Datestamp
from pangu.particle.datestamp.time import Time
from pangu.particle.duration import Duration


def test_init_and_repr():
    t = Time(14, 30)
    assert t.hour == 14
    assert t.minute == 30
    assert "Time(hour=14" in repr(t)


def test_now():
    now = Time.now()
    assert isinstance(now, Time)


def test_add_duration():
    t = Time(14, 0)
    result = t + Duration(minute=30)
    assert isinstance(result, Time)
    assert result.minute == 30


def test_sub_duration():
    t = Time(14, 30)
    result = t - Duration(minute=15)
    assert result.minute == 15


def test_sub_time():
    t1 = Time(15, 0)
    t2 = Time(14, 0)
    diff = t1 - t2
    assert diff.hour == 1


def test_invalid_add():
    t = Time(14)
    with pytest.raises(TypeError):
        _ = t + 123


def test_from_string_default_format():
    t = Time.from_string("14:45:30")
    assert t.hour == 14
    assert t.minute == 45
    assert t.second == 30


def test_from_string_custom_format():
    t = Time.from_string("02|15", "%H|%M")
    assert t.hour == 2
    assert t.minute == 15


def test_from_timestamp():
    ts = datetime(2025, 3, 28, 22, 30, tzinfo=pytz.UTC).timestamp()
    t = Time.from_timestamp(ts, time_zone_name="UTC")
    assert t.hour == 22
    assert t.minute == 30


def test_to_datestamp_all_fields():
    t = Time(15, 45, 10, 250000)
    d = t.to_datestamp(year=2025, month=4, day=5, time_zone_name="UTC")
    assert isinstance(d, Datestamp)
    assert d.year == 2025
    assert d.month == 4
    assert d.day == 5
    assert d.hour == 15
    assert d.minute == 45
    assert d.microsecond == 250000
    assert d.time_zone.zone == "UTC"


def test_to_datestamp_partial_fields():
    t = Time(8, 15, 0)
    d = t.to_datestamp(day=20)
    assert d.hour == 8
    assert d.day == 20


def test_to_datestamp_default_inheritance():
    t = Time(6, 0, 0)
    d = t.to_datestamp()
    assert d.hour == 6
    assert d.day == t.day  # inherited from original datetime


def test_export():
    t = Time(14, 30)
    exported = t.export()
    assert exported["hour"] == 14
    assert exported["minute"] == 30
    assert exported["second"] == 0
    assert exported["microsecond"] == 0
    assert "time_zone_name" in exported