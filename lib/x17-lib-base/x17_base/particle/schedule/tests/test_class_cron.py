import pytest
from datetime import datetime
from x17_base.particle.datestamp import Datestamp
from x17_base.particle.schedule.cron import Cron


def test_cron_validate_valid():
    assert Cron.validate("0 9 * * ? *") is True


def test_cron_validate_invalid():
    assert Cron.validate("invalid-cron") is False


def test_cron_from_str_and_export():
    cron = Cron.from_str("0 9 * * ? *", time_zone_name="Australia/Sydney")
    exported = cron.export()
    assert exported["expression"] == "0 9 * * ? *"
    assert exported["time_zone_name"] == "Australia/Sydney"
    assert isinstance(exported["minutes"], list)


def test_cron_str_and_repr():
    cron = Cron.from_str("15 14 * * ? *")
    assert str(cron) == "15 14 * * ? *"
    assert "expression='15 14 * * ? *" in repr(cron)


def test_cron_eq_and_ne():
    c1 = Cron.from_str("0 12 * * ? *")
    c2 = Cron.from_str("0 12 * * ? *")
    c3 = Cron.from_str("0 9 * * ? *")
    assert c1 == c2
    assert c1 != c3


def test_cron_schedule_next_and_prev_consistency():
    cron = Cron.from_str("0 9 * * ? *", time_zone_name="UTC")
    start = Datestamp(2025, 5, 22, 8, 0, 0, time_zone_name="UTC")
    next_time = cron.get_schedules_next(start=start, count=1)[0]
    prev_time = cron.get_schedules_prev(start=next_time, count=1)[0]
    assert prev_time < next_time


def test_cron_schedule_between():
    cron = Cron.from_str("0 9 * * ? *", time_zone_name="UTC")
    start = Datestamp(2025, 5, 20, 0, 0, 0, time_zone_name="UTC")
    end = Datestamp(2025, 5, 23, 0, 0, 0, time_zone_name="UTC")
    results = cron.get_schedules_between(start=start, end=end)
    assert len(results) >= 2
    assert all(isinstance(dt, Datestamp) for dt in results)
    