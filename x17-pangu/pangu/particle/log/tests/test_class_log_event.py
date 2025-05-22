import pytest
from pangu.particle.log.log_event import LogEvent
from pangu.particle.datestamp import Datestamp


def test_creation():
    event = LogEvent(message="System started", name="init", level="info")
    assert isinstance(event.id, str)
    assert event.message == "System started"
    assert event.level == "INFO"
    assert "init" in event.name
    assert event.datestamp is not None


def test_repr_str():
    event = LogEvent(message="Hello", name="check")
    assert isinstance(repr(event), str)
    assert isinstance(str(event), str)


def test_dict_export():
    event = LogEvent(message="Export test", name="exporter", level="warning")
    d = event.dict
    assert isinstance(d, dict)
    assert d["level"] == "WARNING"
    assert d["message"] == "Export test"
    assert "exporter" in d["name"]
    assert event.export() == d


def test_from_dict():
    cur_dtp = Datestamp.now()
    input_dict = {
        "message": "Loaded from dict",
        "level": "debug",
        "datestamp": cur_dtp,
    }
    base = LogEvent("fallback")
    event = base.from_dict(input_dict)
    assert isinstance(event, LogEvent)
    assert event.message == "Loaded from dict"
    assert event.level == "DEBUG"
    assert event.datestamp == cur_dtp.datestamp_str
    assert event.time_zone_name == cur_dtp.time_zone_name
    
def test_extra_attributes():
    event = LogEvent(message="Extra test", name="extra", level="info", extra={"key": "value"})
    assert event.extra["key"] == "value"
    assert event.extra["key"] != "wrong_value"
    assert event.extra.get("non_existent_key") is None
    
