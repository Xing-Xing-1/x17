from x17.moto.particle.constant import TIME_UNIT_TABLE # type: ignore
from x17.moto.particle.duration import duration # type: ignore

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

