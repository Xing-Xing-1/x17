#!/usr/bin/python
# -*- coding: utf-8 -*-

from moto.particle.constant import TIME_UNIT_TABLE  # type: ignore
from moto.particle.duration import duration  # type: ignore


def test_class():
    assert True == True


def test_class_init():
    duration_obj = duration(1)
    assert duration_obj.duration == 1
    assert duration_obj.unit == "second"


def test_class_str():
    duration_obj = duration(1)
    assert str(duration_obj) == "1 second"
    duration_obj = duration(1, "minute")
    assert str(duration_obj) == "1 minute"


def test_class_dict():
    duration_obj = duration(1)
    assert duration_obj.__dict__() == {
        "duration": 1,
        "unit": "second",
    }
    duration_obj = duration(1, "minute")
    assert duration_obj.__dict__() == {
        "duration": 1,
        "unit": "minute",
    }


def test_class_round_to():
    duration_obj = duration(1)
    assert duration_obj.round_to(1.2345, 2) == 1.23
    assert duration_obj.round_to(1.2345, 1) == 1.2
    assert duration_obj.round_to(1.2345, 0) == 1


def test_class_to_second():
    duration_obj = duration(1, "minute")
    assert duration_obj.to_second() == 60


def test_class_to_minute():
    duration_obj = duration(1)
    assert duration_obj.to_minute() == 1 / 60
    assert duration_obj.to_minute(2) == round(1 / 60, 2)


def test_class_to_hour():
    duration_obj = duration(100)
    assert duration_obj.to_hour() == 100 / 3600
    assert duration_obj.to_hour(2) == round(100 / 3600, 2)
    duration_obj = duration(100000)
    assert duration_obj.to_hour() == 100000 / 3600
    assert duration_obj.to_hour(2) == round(100000 / 3600, 2)


def test_class_to_day():
    duration_obj = duration(100)
    assert duration_obj.to_day() == 100 / 86400
    assert duration_obj.to_day(2) == round(100 / 86400, 2)
    duration_obj = duration(100000)
    assert duration_obj.to_day() == 100000 / 86400
    assert duration_obj.to_day(2) == round(100000 / 86400, 2)


def test_class_to_week():
    duration_obj = duration(100)
    assert duration_obj.to_week() == 100 / 604800
    assert duration_obj.to_week(2) == round(100 / 604800, 2)
    duration_obj = duration(100000)
    assert duration_obj.to_week() == 100000 / 604800
    assert duration_obj.to_week(2) == round(100000 / 604800, 2)


def test_class_to_month():
    duration_obj = duration(100)
    assert duration_obj.to_month() == 100 / 2592000
    assert duration_obj.to_month(2) == round(100 / 2592000, 2)
    duration_obj = duration(100000)
    assert duration_obj.to_month() == 100000 / 2592000
    assert duration_obj.to_month(2) == round(100000 / 2592000, 2)


def test_class_to_year():
    duration_obj = duration(100)
    assert duration_obj.to_year() == 100 / 31536000
    assert duration_obj.to_year(2) == round(100 / 31536000, 2)
    duration_obj = duration(100000)
    assert duration_obj.to_year() == 100000 / 31536000
    assert duration_obj.to_year(2) == round(100000 / 31536000, 2)


def test_class_as_second():
    duration_obj = duration(1)
    duration_obj.as_second()
    assert duration_obj.get_duration() == 1
    assert duration_obj.unit == "second"
    duration_obj = duration(1, "minute")
    duration_obj.as_second()
    assert duration_obj.get_duration() == 60
    assert duration_obj.unit == "second"


def test_class_as_minute():
    duration_obj = duration(1)
    duration_obj.as_minute()
    assert duration_obj.get_duration() == 1 / 60
    assert duration_obj.unit == "minute"
    duration_obj = duration(1, "day")
    duration_obj.as_minute()
    assert duration_obj.get_duration() == 1440
    assert duration_obj.unit == "minute"


def test_class_as_hour():
    duration_obj = duration(1, "day")
    duration_obj.as_hour()
    assert duration_obj.get_duration() == 24
    assert duration_obj.unit == "hour"
    duration_obj = duration(1, "minute")
    duration_obj.as_hour()
    assert duration_obj.get_duration() == 1 / 60
    assert duration_obj.unit == "hour"


def test_class_as_day():
    duration_obj = duration(1200, "minute")
    duration_obj.as_day(round_to=0)
    assert duration_obj.get_duration() == 1
    assert duration_obj.unit == "day"
    duration_obj = duration(1, "second")
    duration_obj.as_day()
    assert duration_obj.get_duration() == 1 / 86400
    assert duration_obj.unit == "day"


def test_class_as_week():
    duration_obj = duration(1, "month")
    duration_obj.as_week(round_to=0)
    assert duration_obj.get_duration() == 4
    assert duration_obj.unit == "week"
    duration_obj = duration(14, "day")
    duration_obj.as_week(round_to=0)
    assert duration_obj.get_duration() == 2
    assert duration_obj.unit == "week"


def test_class_as_month():
    duration_obj = duration(1, "year")
    duration_obj.as_month(round_to=0)
    assert duration_obj.get_duration() == 12
    assert duration_obj.unit == "month"
    duration_obj = duration(4, "week")
    duration_obj.as_month(round_to=0)
    assert duration_obj.get_duration() == 1
    assert duration_obj.unit == "month"


def test_instance_get_duration():
    duration_obj = duration(1)
    assert duration_obj.get_duration() == 1


def test_instance_get_unit():
    duration_obj = duration(1)
    assert duration_obj.get_unit() == "second"


def test_instance_abs():
    duration_obj = duration(-1)
    res = abs(duration_obj)
    assert res.get_duration() == 1
    assert res.get_unit() == "second"


def test_instance_plus():
    duration_obj = duration(1)
    res = duration_obj + duration(1)
    assert res.get_duration() == 2
    assert res.get_unit() == "second"


def test_instance_minus():
    duration_obj = duration(1)
    res = duration_obj - duration(1)
    assert res.get_duration() == 0
    assert res.get_unit() == "second"
    duration_obj = duration(1, "minute")
    res = duration_obj - duration(1, "second")
    assert res.get_duration() == 59
    assert res.get_unit() == "second"
    duration_obj = duration(1, "hour")
    res = duration_obj - duration(1, "minute")
    assert res.get_duration() == 59
    assert res.get_unit() == "minute"
    duration_obj = duration(1, "hour")
    res = duration_obj - duration(1, "day")
    assert res.get_duration() == -23 / 24
    assert res.get_unit() == "day"


def test_instance_multiply():
    duration_obj = duration(1)
    res = duration_obj * 2
    assert res.get_duration() == 2
    assert res.get_unit() == "second"
    duration_obj = duration(1, "minute")
    res = duration_obj * 2
    assert res.get_duration() == 2
    assert res.get_unit() == "minute"
