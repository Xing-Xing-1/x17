import pytest
from unittest.mock import MagicMock

from pangu.particle.log.log_stream import LogStream
from pangu.particle.log.log_event import LogEvent


def test_logstream_creation():
    stream = LogStream(name="test_logger", format="[%(message)s]", verbose=True)
    assert isinstance(stream.id, str)
    assert stream.base_name == "test_logger"
    assert stream.name == "test_logger"
    assert stream.log_format == "[%(message)s]"
    assert hasattr(stream, "log_node")
    assert stream.verbose is True


def test_logstream_repr_str():
    stream = LogStream(name="mylog")
    assert isinstance(repr(stream), str)
    assert isinstance(str(stream), str)
    assert "mylog" in str(stream)
    assert "LogStream" in repr(stream)


def test_logstream_dict():
    stream = LogStream(name="abc", format="[%(message)s]", verbose=True)
    d = stream.dict
    assert isinstance(d, dict)
    for key in stream.attr:
        assert key in d


def test_logstream_log_to_group():
    mock_group = MagicMock()
    stream = LogStream(name="grouped", group=mock_group)
    stream.log(message="hello world", level="INFO")
    mock_group.receive.assert_called_once()
    name_arg, event_arg = mock_group.receive.call_args[0]
    assert name_arg == "grouped"
    assert isinstance(event_arg, LogEvent)
    assert event_arg.message == "hello world"
    assert event_arg.level == "INFO"


@pytest.mark.parametrize("method,level", [
    ("debug", "DEBUG"),
    ("info", "INFO"),
    ("error", "ERROR"),
    ("critical", "CRITICAL"),
])
def test_logstream_level_helpers(method, level):
    stream = LogStream(name="leveltest", verbose=False)
    log_method = getattr(stream, method)
    # Monkeypatch the real .log method to intercept the call
    stream.log = MagicMock()
    log_method("test message")
    stream.log.assert_called_once()
    assert stream.log.call_args[1]["level"] == level
    

def test_logstream_memory_append_if_no_group():
    stream = LogStream(name="memtest", verbose=False)
    assert len(stream.memory) == 0
    stream.log("testing memory store")
    assert len(stream.memory) == 1
    event = stream.memory[0]
    assert isinstance(event, LogEvent)
    assert event.message == "testing memory store"


def test_logstream_does_not_append_memory_if_group():
    mock_group = MagicMock()
    stream = LogStream(name="nogroupmem", group=mock_group, verbose=False)
    stream.log("hello with group")
    assert len(stream.memory) == 0
    mock_group.receive.assert_called_once()


def test_logstream_export_structure():
    stream = LogStream(name="exportlog", verbose=False)
    stream.log("first log")
    stream.log("second log")
    export = stream.export()
    assert export["name"] == "exportlog"
    assert isinstance(export["logs"], list)
    assert len(export["logs"]) == 2
    assert all(isinstance(log, dict) for log in export["logs"])
    assert export["group"] is None
    assert export["verbose"] is False
    
@pytest.mark.parametrize("method", ["info", "error", "critical", "debug"])
def test_helper_methods_store_to_memory(method):
    stream = LogStream(name=f"{method}-test", verbose=False)
    call = getattr(stream, method)
    call("helper call test")
    assert len(stream.memory) == 1
    assert stream.memory[0].level == method.upper()
    assert stream.memory[0].message == "helper call test"
    
    