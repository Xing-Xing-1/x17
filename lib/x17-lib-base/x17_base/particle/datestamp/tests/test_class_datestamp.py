#!/usr/bin/python
# -*- coding: utf-8 -*-
from datetime import datetime
import pytest
import pytz

from x17_base.particle.datestamp import Datestamp
from x17_base.particle.duration.duration import Duration


def test_init_basic():
    ds = Datestamp(2025, 3, 23, 15, 30)
    assert ds.year == 2025
    assert ds.month == 3
    assert ds.day == 23
    assert ds.hour == 15
    assert ds.minute == 30


def test_configure_and_get_format():
    Datestamp.configure(
        date_format="%d/%m/%Y",
        time_format="%H-%M-%S",
        date_time_format="%d/%m/%Y %H-%M-%S",
        time_zone_name="Asia/Tokyo",
    )
    assert Datestamp.get_date_format() == "%d/%m/%Y"
    assert Datestamp.get_time_format() == "%H-%M-%S"
    assert Datestamp.get_date_time_format() == "%d/%m/%Y %H-%M-%S"
    assert Datestamp.get_time_zone_name() == "Asia/Tokyo"


def test_now():
    ds = Datestamp.now()
    assert isinstance(ds, Datestamp)


def test_from_datetime():
    dt = datetime(2022, 12, 31, 23, 59)
    ds = Datestamp.from_datetime(dt, "UTC")
    assert ds.year == 2022
    assert ds.hour == 23


def test_from_timestamp():
    dt = pytz.timezone("UTC").localize(datetime(2024, 1, 1, 12, 0))
    ts = dt.timestamp()
    ds = Datestamp.from_timestamp(ts, "UTC")
    assert ds.year == 2024
    assert ds.hour == 12


def test_from_string():
    ds = Datestamp.from_string("2025-03-23 18:30:00", "%Y-%m-%d %H:%M:%S")
    assert ds.year == 2025
    assert ds.hour == 18


def test_from_dict():
    ds = Datestamp.from_dict({
        "year": 2025, "month": 3, "day": 23, "hour": 10,
        "minute": 5, "second": 45, "time_zone_name": "UTC"
    })
    assert ds.year == 2025
    assert ds.minute == 5


def test_str_output():
    ds = Datestamp(2025, 3, 23, 10, 0, 0)
    assert isinstance(str(ds), str)
    assert "2025" in str(ds)


def test_timezone_awareness():
    ds = Datestamp(2025, 3, 23, 10, 0, 0, time_zone_name="Asia/Shanghai")
    assert ds.time_zone.zone == "Asia/Shanghai"
    assert ds.time_zone_name == "Asia/Shanghai"


def test_dst_transition():
    ds = Datestamp(2024, 3, 31, 2, 0, 0, time_zone_name="Europe/Paris")
    assert ds.time_zone.zone == "Europe/Paris"
    assert ds.hour == 2


def test_repr_formatting():
    ds = Datestamp(2025, 3, 23, 14, 55, 30)
    text = str(ds)
    assert "2025" in text
    assert "14" in text


def test_invalid_timezone():
    with pytest.raises(Exception):
        Datestamp(2025, 3, 23, time_zone_name="Invalid/Zone")


def test_cross_timezone_timestamp():
    ds1 = Datestamp(2025, 3, 23, 10, 0, 0, time_zone_name="UTC")
    ds2 = Datestamp(2025, 3, 23, 10, 0, 0, time_zone_name="Asia/Tokyo")
    assert ds1.datetime.timestamp() != ds2.datetime.timestamp()


def test_configure_timezone_only():
    Datestamp.configure(time_zone_name="America/New_York")
    assert Datestamp.get_time_zone_name() == "America/New_York"


def test_init_all_zero():
    ds = Datestamp(2025, 1, 1)
    assert ds.hour == 0
    assert ds.minute == 0
    assert ds.second == 0
    assert ds.microsecond == 0


def test_configure_partial_format():
    Datestamp.configure(date_format="%Y/%m/%d")
    assert Datestamp.get_date_format() == "%Y/%m/%d"

    Datestamp.configure(time_format="%H:%M")
    assert Datestamp.get_time_format() == "%H:%M"

    Datestamp.configure(date_time_format="%Y/%m/%d %H:%M")
    assert Datestamp.get_date_time_format() == "%Y/%m/%d %H:%M"

    Datestamp.reset()


def test_from_string_with_format_and_timezone():
    ds = Datestamp.from_string(
        "23/03/2025 22-45-00",
        "%d/%m/%Y %H-%M-%S",
        time_zone_name="Asia/Tokyo"
    )
    assert ds.year == 2025
    assert ds.hour == 22
    assert ds.time_zone_name == "Asia/Tokyo"


def test_set_method_on_instance():
    ds = Datestamp(2025, 3, 23)
    ds.set(hour=5, minute=10)
    assert ds.hour == 5
    assert ds.minute == 10
    with pytest.raises(AttributeError):
        ds.set(not_exist=123)


def test_getters():
    ds = Datestamp(2025, 3, 23, 14, 30, 45)
    assert isinstance(ds.get_datetime(), datetime)
    assert isinstance(ds.get_timestamp(), float)


def test_properties():
    ds = Datestamp(2025, 3, 23, 14, 30, 45, time_zone_name="UTC")
    assert isinstance(ds.date_str, str)
    assert isinstance(ds.time_str, str)
    assert isinstance(ds.datestamp_str, str)
    assert ds.dict["year"] == 2025


def test_operator_add_duration():
    ds = Datestamp(2025, 3, 23, 10, 0, 0, time_zone_name="UTC")
    duration = Duration(second=3600)
    new_ds = ds + duration
    assert new_ds.hour == 11


def test_operator_radd_duration():
    ds = Datestamp(2025, 3, 23, 10, 0, 0, time_zone_name="UTC")
    duration = Duration(second=1800)
    new_ds = duration + ds
    assert new_ds.minute == 30


def test_operator_sub_duration():
    ds = Datestamp(2025, 3, 23, 10, 0, 0, time_zone_name="UTC")
    duration = Duration(second=600)
    new_ds = ds - duration
    assert new_ds.minute == 50


def test_operator_sub_datestamp():
    ds1 = Datestamp(2025, 3, 23, 11, 0, 0, time_zone_name="UTC")
    ds2 = Datestamp(2025, 3, 23, 10, 0, 0, time_zone_name="UTC")
    duration = ds1 - ds2
    assert duration.base == 3600


def test_operator_comparisons():
    ds1 = Datestamp(2025, 3, 23, 11, 0, 0)
    ds2 = Datestamp(2025, 3, 23, 10, 0, 0)
    assert ds1 > ds2
    assert ds2 < ds1
    assert ds1 >= ds2
    assert ds2 <= ds1
    assert ds1 != ds2
    assert not ds1 == ds2


def test_operator_bool_and_hash():
    ds = Datestamp(2025, 1, 1)
    assert bool(ds)
    assert isinstance(hash(ds), int)


def test_describe_and_export():
    ds = Datestamp(2025, 3, 23, 12, 34, 56)
    desc = ds.describe()
    text = ds.describe(as_text=True)
    assert "year" in desc
    assert "12 hour" in text


def test_export():
    ds = Datestamp(2025, 3, 23, 12, 34, 56)
    exported = ds.export()
    assert exported["year"] == 2025
    assert exported["month"] == 3
    assert exported["day"] == 23
    assert exported["hour"] == 12
    assert exported["minute"] == 34
    assert exported["second"] == 56
    assert exported["time_zone_name"] == "Australia/Sydney"


def test_reimport():
    ds = Datestamp(2025, 3, 23, 12, 34, 56)
    exported = ds.export()
    reimported = Datestamp.from_dict(exported)
    assert reimported.year == 2025
    assert reimported.month == 3
    assert reimported.day == 23
    assert reimported.hour == 12
    assert reimported.minute == 34
    assert reimported.second == 56