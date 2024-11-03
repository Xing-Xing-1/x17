from moto.particle.date_time import date_time # type: ignore
from moto.particle.duration import duration # type: ignore
from moto.particle.constant import TIMEZONE_TABLE # type: ignore 
from datetime import datetime
import pytz  # type: ignore

def test_class():
	assert date_time.TIME_ZONE == pytz.timezone("Australia/Sydney")
	assert date_time.DATE_FORMAT == "%Y-%m-%d"
	assert date_time.TIME_FORMAT == "%H:%M:%S"
	assert date_time.DATE_TIME_FORMAT == "%Y-%m-%d %H:%M:%S"

def test_class_show_time_zones():
	assert date_time.show_time_zones() == TIMEZONE_TABLE

def test_class_set_timezone():
	date_time.set_timezone(pytz.timezone("Australia/Melbourne"))
	assert date_time.TIME_ZONE == pytz.timezone("Australia/Melbourne")

def test_class_set_time_format():
	date_time.set_time_format("%H:%M")
	assert date_time.TIME_FORMAT == "%H:%M"
	date_time.set_time_format("%H:%M:%S")

def test_class_set_date_format():
	date_time.set_date_format("%d-%m-%Y")
	assert date_time.DATE_FORMAT == "%d-%m-%Y"
	date_time.set_date_format("%Y-%m-%d")

def test_class_set_date_time_format():
	date_time.set_date_time_format("%d-%m-%Y %H:%M")
	assert date_time.DATE_TIME_FORMAT == "%d-%m-%Y %H:%M"
	date_time.set_date_time_format("%Y-%m-%d %H:%M:%S")

def test_class_from_str():
	date_time_str = "2021-01-01 00:00:00"
	date_time_obj = date_time.from_str(date_time_str = date_time_str)
	result = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo = date_time.TIME_ZONE)
	assert date_time_obj.date_time == result

def test_class_from_timestamp():
	timestamp = 1609459200
	date_time_obj = date_time.from_timestamp(timestamp)
	result = datetime.fromtimestamp(timestamp, date_time.TIME_ZONE).replace(tzinfo = date_time.TIME_ZONE)
	assert date_time_obj.date_time == result

def test_instance_set():
	date_time_str = "2021-01-01 00:00:00"
	date_time_obj = date_time()
	date_time_obj.set(
		datetime_obj = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S"),
		date_format = "%d-%m-%Y",
		time_format = "%H:%M",
		date_time_format = "%d-%m-%Y %H:%M",
		time_zone = pytz.timezone("Australia/Melbourne"),
	)
	result = datetime.strptime(date_time_str, "%Y-%m-%d %H:%M:%S").replace(tzinfo = pytz.timezone("Australia/Melbourne"))
	assert date_time_obj.date_time == result
	assert date_time_obj.date_format == "%d-%m-%Y"
	assert date_time_obj.time_format == "%H:%M"
	assert date_time_obj.date_time_format == "%d-%m-%Y %H:%M"
	assert date_time_obj.time_zone == pytz.timezone("Australia/Melbourne")

def test_instance_str():
	date_time_str = "2021-01-01 00:00:00"
	date_time_obj = date_time.from_str(date_time_str = date_time_str)
	assert str(date_time_obj) == date_time_str

def test_instance_dict():
	date_time_str = "2021-01-01 00:00:00"
	date_time_obj = date_time.from_str(date_time_str = date_time_str)
	assert date_time_obj.__dict__() == {
		"date_time": "2021-01-01 00:00:00",
		"time_zone": date_time_obj.time_zone,
	}

def test_instance_get_date_str():
	date_time_str = "2021-01-01 00:00:00"
	date_time_obj = date_time.from_str(date_time_str = date_time_str)
	assert date_time_obj.get_date_str() == "2021-01-01"

def test_instance_get_time_str():
	date_time_str = "2021-01-01 00:00:00"
	date_time_obj = date_time.from_str(date_time_str = date_time_str)
	assert date_time_obj.get_time_str() == "00:00:00"

def test_instance_get_date_time_str():
	date_time_str = "2021-01-01 00:00:00"
	date_time_obj = date_time.from_str(date_time_str = date_time_str)
	assert date_time_obj.get_date_time_str() == "2021-01-01 00:00:00"

def test_instance_get_timestamp():
	date_time_str = "2021-01-01 00:00:00"
	date_time_obj = date_time.from_str(date_time_str = date_time_str)
	assert date_time_obj.get_timestamp() == 1609424400

def test_instance_get_time_zone():
	date_time_str = "2021-01-01 00:00:00"
	date_time_obj = date_time.from_str(date_time_str = date_time_str)
	assert date_time_obj.get_time_zone() == date_time.TIME_ZONE

def test_instance_get_date():
	date_time_str = "2021-01-01 00:00:00"
	date_time_obj = date_time.from_str(date_time_str = date_time_str)
	assert date_time_obj.get_date() == datetime.strptime("2021-01-01", "%Y-%m-%d").date()

def test_instance_get_time():
	date_time_str = "2021-01-01 00:00:00"
	date_time_obj = date_time.from_str(date_time_str = date_time_str)
	assert date_time_obj.get_time() == datetime.strptime("00:00:00", "%H:%M:%S").time()

def get_date_time():
	date_time_str = "2021-01-01 00:00:00"
	date_time_obj = date_time.from_str(date_time_str = date_time_str)
	assert date_time_obj.get_date_time() == datetime.strptime("2021-01-01 00:00:00", "%Y-%m-%d %H:%M:%S")

'''
	Operations:

'''

def test_instance_add():
	duration_obj = duration(60, "minute")
	date_time_str = "2021-01-01 00:00:00"
	date_time_obj = date_time.from_str(date_time_str = date_time_str)
	res = date_time_obj + duration_obj
	assert res.get_date_time_str() == "2021-01-01 01:00:00"

def test_instance_sub():
	duration_obj = duration(60, "minute")
	date_time_str = "2021-01-01 00:00:00"
	date_time_obj = date_time.from_str(date_time_str = date_time_str)
	res = date_time_obj - duration_obj
	assert res.get_date_time_str() == "2020-12-31 23:00:00"

def test_instance_diff():
	date_time_str1 = "2021-01-01 00:00:00"
	date_time_obj1 = date_time.from_str(date_time_str = date_time_str1)
	date_time_str2 = "2021-01-01 01:00:00"
	date_time_obj2 = date_time.from_str(date_time_str = date_time_str2)
	res = date_time_obj1.diff(date_time_obj2)
	assert isinstance(res, duration)
	assert res.get_duration() == -3600
	assert res.unit == "second"
	res = date_time_obj2.diff(date_time_obj1, absolute=True)
	assert isinstance(res, duration)
	assert res.get_duration() == 3600
	assert res.unit == "second"



