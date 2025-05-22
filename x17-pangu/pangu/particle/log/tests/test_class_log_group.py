import time
from unittest.mock import MagicMock
import pytest

from pangu.particle.log.log_group import LogGroup
from pangu.particle.log.log_stream import LogStream
from pangu.particle.log.log_event import LogEvent


def test_register_stream_sets_group_and_stream_dict():
    group = LogGroup(name="main")
    stream = LogStream(name="mylogger")
    group.register_stream(stream)

    assert stream.group == group
    assert "mylogger" in group.streams
    assert isinstance(group.streams["mylogger"], list)


def test_sync_receive_appends_event_and_pushes_to_core():
    core = MagicMock()
    group = LogGroup(name="sync-group", core=core, sync=True)
    event = LogEvent(message="Sync test", name="sync-group", level="INFO")

    group.receive("stream1", event)

    assert "stream1" in group.streams
    assert group.streams["stream1"][0] == event
    core.push.assert_called_once_with("sync-group", "stream1", event)


def test_async_receive_enqueue_and_later_flushes():
    group = LogGroup(name="async-group", sync=False)
    event = LogEvent(message="Async test", name="async-group", level="DEBUG")

    group.receive("stream2", event)
    time.sleep(0.1)

    assert "stream2" in group.streams
    assert len(group.streams["stream2"]) == 1
    assert group.streams["stream2"][0].message == "Async test"


def test_export_returns_correct_structure():
    group = LogGroup(name="export-group", sync=True)
    event = LogEvent(message="Exported", name="export-group", level="INFO")
    group.receive("export-stream", event)

    exported = group.export()
    assert isinstance(exported, dict)
    assert "export-stream" in exported
    assert isinstance(exported["export-stream"], list)
    assert exported["export-stream"][0]["message"] == "Exported"


def test_repr_and_dict_and_attr():
    group = LogGroup(name="debug-group")
    assert isinstance(repr(group), str)
    assert isinstance(str(group), str)

    d = group.dict
    assert "name" in d and d["name"] == "debug-group"

    attrs = group.attr
    assert isinstance(attrs, list)
    assert "name" in attrs