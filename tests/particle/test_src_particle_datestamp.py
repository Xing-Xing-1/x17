from datetime import datetime

import pytz  # type: ignore

from moto.particle.constant import TIMEZONE_TABLE
from moto.particle.datestamp import datestamp
from moto.particle.duration import duration


def test_class():
    assert datestamp.TIME_ZONE == pytz.timezone("Australia/Sydney")
    assert datestamp.DATE_FORMAT == "%Y-%m-%d"
    assert datestamp.TIME_FORMAT == "%H:%M:%S"
    assert datestamp.datestamp_FORMAT == "%Y-%m-%d %H:%M:%S"


def test_class_show_time_zones():
    assert datestamp.show_time_zones() == TIMEZONE_TABLE


def test_class_set_timezone():
    datestamp.set_timezone(pytz.timezone("Australia/Melbourne"))
    assert datestamp.TIME_ZONE == pytz.timezone("Australia/Melbourne")


def test_class_set_time_format():
    datestamp.set_time_format("%H:%M")
    assert datestamp.TIME_FORMAT == "%H:%M"
    datestamp.set_time_format("%H:%M:%S")


def test_class_set_date_format():
    datestamp.set_date_format("%d-%m-%Y")
    assert datestamp.DATE_FORMAT == "%d-%m-%Y"
    datestamp.set_date_format("%Y-%m-%d")


def test_class_set_datestamp_format():
    datestamp.set_datestamp_format("%d-%m-%Y %H:%M")
    assert datestamp.datestamp_FORMAT == "%d-%m-%Y %H:%M"
    datestamp.set_datestamp_format("%Y-%m-%d %H:%M:%S")


def test_class_from_str():
    datestamp_str = "2021-01-01 00:00:00"
    datestamp_obj = datestamp.from_str(datestamp_str=datestamp_str)
    result = datetime.strptime(datestamp_str, "%Y-%m-%d %H:%M:%S").replace(
        tzinfo=datestamp.TIME_ZONE
    )
    assert datestamp_obj.datestamp == result


def test_class_from_timestamp():
    timestamp = 1609459200
    datestamp_obj = datestamp.from_timestamp(timestamp)
    result = datetime.fromtimestamp(timestamp, datestamp.TIME_ZONE).replace(
        tzinfo=datestamp.TIME_ZONE
    )
    assert datestamp_obj.datestamp == result


def test_instance_set():
    datestamp_str = "2021-01-01 00:00:00"
    datestamp_obj = datestamp()
    datestamp_obj.set(
        datetime_obj=datetime.strptime(datestamp_str, "%Y-%m-%d %H:%M:%S"),
        date_format="%d-%m-%Y",
        time_format="%H:%M",
        datestamp_format="%d-%m-%Y %H:%M",
        time_zone=pytz.timezone("Australia/Melbourne"),
    )
    result = datetime.strptime(datestamp_str, "%Y-%m-%d %H:%M:%S").replace(
        tzinfo=pytz.timezone("Australia/Melbourne")
    )
    assert datestamp_obj.datestamp == result
    assert datestamp_obj.date_format == "%d-%m-%Y"
    assert datestamp_obj.time_format == "%H:%M"
    assert datestamp_obj.datestamp_format == "%d-%m-%Y %H:%M"
    assert datestamp_obj.time_zone == pytz.timezone("Australia/Melbourne")


def test_instance_str():
    datestamp_str = "2021-01-01 00:00:00"
    datestamp_obj = datestamp.from_str(datestamp_str=datestamp_str)
    assert str(datestamp_obj) == datestamp_str


def test_instance_dict():
    datestamp_str = "2021-01-01 00:00:00"
    datestamp_obj = datestamp.from_str(datestamp_str=datestamp_str)
    assert datestamp_obj.__dict__() == {
        "datestamp": "2021-01-01 00:00:00",
        "time_zone": datestamp_obj.time_zone,
    }


def test_instance_get_date_str():
    datestamp_str = "2021-01-01 00:00:00"
    datestamp_obj = datestamp.from_str(datestamp_str=datestamp_str)
    assert datestamp_obj.get_date_str() == "2021-01-01"


def test_instance_get_time_str():
    datestamp_str = "2021-01-01 00:00:00"
    datestamp_obj = datestamp.from_str(datestamp_str=datestamp_str)
    assert datestamp_obj.get_time_str() == "00:00:00"


def test_instance_get_datestamp_str():
    datestamp_str = "2021-01-01 00:00:00"
    datestamp_obj = datestamp.from_str(datestamp_str=datestamp_str)
    assert datestamp_obj.get_datestamp_str() == "2021-01-01 00:00:00"


def test_instance_get_timestamp():
    datestamp_str = "2021-01-01 00:00:00"
    datestamp_obj = datestamp.from_str(datestamp_str=datestamp_str)
    assert datestamp_obj.get_timestamp() == 1609424400


def test_instance_get_time_zone():
    datestamp_str = "2021-01-01 00:00:00"
    datestamp_obj = datestamp.from_str(datestamp_str=datestamp_str)
    assert datestamp_obj.get_time_zone() == datestamp.TIME_ZONE


def test_instance_get_date():
    datestamp_str = "2021-01-01 00:00:00"
    datestamp_obj = datestamp.from_str(datestamp_str=datestamp_str)
    assert (
        datestamp_obj.get_date() == datetime.strptime("2021-01-01", "%Y-%m-%d").date()
    )


def test_instance_get_time():
    datestamp_str = "2021-01-01 00:00:00"
    datestamp_obj = datestamp.from_str(datestamp_str=datestamp_str)
    assert datestamp_obj.get_time() == datetime.strptime("00:00:00", "%H:%M:%S").time()


def get_datestamp():
    datestamp_str = "2021-01-01 00:00:00"
    datestamp_obj = datestamp.from_str(datestamp_str=datestamp_str)
    assert datestamp_obj.get_datestamp() == datetime.strptime(
        "2021-01-01 00:00:00", "%Y-%m-%d %H:%M:%S"
    )


"""
	Operations:

"""


def test_instance_add():
    duration_obj = duration(60, "minute")
    datestamp_str = "2021-01-01 00:00:00"
    datestamp_obj = datestamp.from_str(datestamp_str=datestamp_str)
    res = datestamp_obj + duration_obj
    assert res.get_datestamp_str() == "2021-01-01 01:00:00"


def test_instance_sub():
    duration_obj = duration(60, "minute")
    datestamp_str = "2021-01-01 00:00:00"
    datestamp_obj = datestamp.from_str(datestamp_str=datestamp_str)
    res = datestamp_obj - duration_obj
    assert res.get_datestamp_str() == "2020-12-31 23:00:00"


def test_instance_diff():
    datestamp_str1 = "2021-01-01 00:00:00"
    datestamp_obj1 = datestamp.from_str(datestamp_str=datestamp_str1)
    datestamp_str2 = "2021-01-01 01:00:00"
    datestamp_obj2 = datestamp.from_str(datestamp_str=datestamp_str2)
    res = datestamp_obj1.diff(datestamp_obj2)
    assert isinstance(res, duration)
    assert res.get_duration() == -3600
    assert res.unit == "second"
    res = datestamp_obj2.diff(datestamp_obj1, absolute=True)
    assert isinstance(res, duration)
    assert res.get_duration() == 3600
    assert res.unit == "second"
