#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import timedelta
from dateutil.relativedelta import relativedelta  # type: ignore

from x17_base.particle.duration.duration import Duration


def test_init():
    d = Duration(year=1, day=2, second=30)
    assert d.year == 1
    assert d.day == 2
    assert d.second == 30

def test_dict():
    d = Duration(minute=3)
    assert "minute" in d.dict
    assert d.dict["minute"] == 3

def test_base():
    d = Duration(hour=1)
    assert d.base == 3600

def test_normalize():
    d = Duration(second=90)
    d.as_normalize()
    assert d.minute == 1
    assert d.second == 30

def test_add():
    d1 = Duration(day=1, hour=2)
    d2 = Duration(hour=1)
    d3 = d1 + d2
    assert d3.hour == 3
    assert d3.day == 1

def test_sub():
    d1 = Duration(day=1, hour=3)
    d2 = Duration(hour=1)
    d3 = d1 - d2
    assert d3.hour == 2

def test_eq():
    d1 = Duration(minute=5)
    d2 = Duration(minute=5)
    assert d1 == d2

def test_ne():
    d1 = Duration(minute=5)
    d2 = Duration(minute=3)
    assert d1 != d2

def test_comparison():
    d1 = Duration(second=30)
    d2 = Duration(second=60)
    assert d1 < d2
    assert d2 > d1
    assert d1 <= d2
    assert d2 >= d1

def test_radd():
    d1 = Duration(second=10)
    result = sum([d1, d1], Duration())
    assert result.second == 20

def test_mul():
    d = Duration(minute=2)
    result = d * 3
    assert result.minute == 6

def test_truediv():
    d = Duration(minute=10)
    result = d / 2
    assert result.minute == 5

def test_from_dict():
    d = Duration.from_dict({"hour": 2, "minute": 30})
    assert d.hour == 2
    assert d.minute == 30

def test_from_timedelta():
    td = timedelta(days=2, seconds=3600)
    d = Duration.from_timedelta(td)
    assert d.day == 2
    assert d.hour == 1

def test_from_relativedelta():
    rd = relativedelta(years=1, months=2, days=3)
    d = Duration.from_relativedelta(rd)
    assert d.year == 1
    assert d.month == 2
    assert d.day == 3

def test_describe_basic():
    d = Duration(year=1, month=2, day=3, minute=1)
    desc = d.describe(as_text=True)
    assert "1 year" in desc
    assert "2 month" in desc
    assert "3 day" in desc
    assert "1 minute" in desc

def test_describe_zero():
    d = Duration()
    assert d.describe(as_text=True) == "0 second"

def test_describe_singular_plural():
    d = Duration(year=1, month=1, day=1, second=1)
    assert d.describe(as_text=True) == "1 year, 1 month, 1 day, 1 second"
    d2 = Duration(year=2, month=3, second=0)
    assert d2.describe(as_text=True) == "2 year, 3 month"

def test_describe_as_dict():
    d = Duration(year=1, month=2, day=3)
    desc = d.describe(as_text=False)
    assert desc["year"] == 1
    assert desc["month"] == 2
    assert desc["day"] == 3

def test_describe_as_dict_zero():
    d = Duration()
    desc = d.describe(as_text=False)
    assert desc["second"] == 0
    assert desc["minute"] == 0
    assert desc["hour"] == 0
    assert desc["day"] == 0
    assert desc["month"] == 0
    assert desc["year"] == 0
    assert desc["microsecond"] == 0
    assert desc["week"] == 0

def test_export():
    d = Duration(year=1, month=2, day=3)
    export_data = d.export()
    assert export_data["year"] == 1
    assert export_data["month"] == 2
    assert export_data["day"] == 3
    assert export_data["hour"] == 0
    assert export_data["minute"] == 0
    assert export_data["second"] == 0
    assert export_data["microsecond"] == 0
    assert export_data["nanosecond"] == 0

    d2 = Duration.from_dict(export_data)
    assert d2.year == 1
    assert d2.month == 2
    assert d2.day == 3
    assert d2.hour == 0
    assert d2.minute == 0

def test_set_method_updates_fields():
    d = Duration()
    d.set(year=2, second=30, hour=1)
    assert d.year == 2
    assert d.second == 30
    assert d.hour == 1

def test_set_method_ignores_invalid_keys():
    d = Duration()
    d.set(invalid_key=123)  # should not raise error
    assert not hasattr(d, "invalid_key")

def test_set_precise_mode():
    Duration.set_precise()
    d = Duration(year=1)
    approx_seconds = 365.25 * 86400
    assert abs(d.base - approx_seconds) <= 5000

def test_nanosecond_initialization():
    d = Duration(nanosecond=999)
    assert d.nanosecond == 999

def test_nanosecond_in_dict_and_export():
    d = Duration(nanosecond=500)
    assert d.dict["nanosecond"] == 500
    assert d.export()["nanosecond"] == 500

def test_hash_and_bool():
    d1 = Duration(minute=1)
    d2 = Duration()
    assert bool(d1)
    assert not bool(d2)
    assert isinstance(hash(d1), int)

def test_repr_and_str_output():
    d = Duration(year=1, day=2)
    text = str(d)
    assert "year=1" in text
    assert "day=2" in text

def test_add_timedelta():
    d1 = Duration(second=30)
    td = timedelta(seconds=45)
    result = d1 + td
    assert result.second == 15
    assert result.minute == 1
    assert result.hour == 0

def test_add_relativedelta():
    d1 = Duration(month=1)
    rd = relativedelta(months=2)
    result = d1 + rd
    assert result.month == 3

def test_sub_timedelta():
    d1 = Duration(minute=3)
    td = timedelta(seconds=60)
    result = d1 - td
    assert result.second >= 0
    assert result.minute == 2