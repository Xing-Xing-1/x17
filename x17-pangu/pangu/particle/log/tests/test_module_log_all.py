import time
from pangu.particle.log.log_core import LogCore
from pangu.particle.log.log_group import LogGroup
from pangu.particle.log.log_stream import LogStream


def test_full_chain_logging_to_core():
    core = LogCore()
    group = LogGroup(name="group1", core=core)
    stream = LogStream(name="streamA")
    group.register_stream(stream)

    stream.info("System booted")
    time.sleep(0.1)  # 等待核心消费

    logs = core.export("group1", "streamA")
    assert len(logs) == 1
    assert logs[0]["message"] == "System booted"


def test_multiple_streams_multiple_groups():
    core = LogCore()

    g1 = LogGroup(name="g1", core=core)
    g2 = LogGroup(name="g2", core=core)
    s1 = g1.register_stream(LogStream(name="s1"))
    s2 = g1.register_stream(LogStream(name="s2"))
    s3 = g2.register_stream(LogStream(name="s3"))

    s1.debug("msg from s1")
    s2.info("msg from s2")
    s3.error("msg from s3")

    time.sleep(0.2)

    all_exported = core.export()
    assert "g1" in all_exported and "g2" in all_exported
    assert all_exported["g1"]["s1"][0]["message"] == "msg from s1"
    assert all_exported["g1"]["s2"][0]["message"] == "msg from s2"
    assert all_exported["g2"]["s3"][0]["message"] == "msg from s3"


def test_sync_mode_group_logs_directly():
    core = LogCore()
    group = LogGroup(name="sync-group", core=core, sync=True)
    stream = LogStream(name="direct-log")
    group.register_stream(stream)

    stream.critical("CRITICAL HIT!")
    time.sleep(0.1)
    logs = core.export("sync-group", "direct-log")
    assert logs[0]["message"] == "CRITICAL HIT!"


def test_event_flow_calls_core_push(monkeypatch):
    pushed = []

    def mock_push(group, stream, event):
        pushed.append((group, stream, event.message))

    core = LogCore()
    monkeypatch.setattr(core, "push", mock_push)

    group = LogGroup(name="flow-group", core=core, sync=True)
    stream = group.register_stream(LogStream(name="flow-stream"))
    stream.warn("flowing event")

    assert pushed == [("flow-group", "flow-stream", "flowing event")]


def test_core_export_modes():
    core = LogCore()
    g = LogGroup(name="export-group", core=core)
    s = g.register_stream(LogStream(name="export-stream"))
    s.info("E1")
    s.error("E2")
    time.sleep(0.1)

    all_logs = core.export()
    assert list(all_logs.keys()) == ["export-group"]
    assert list(all_logs["export-group"].keys()) == ["export-stream"]
    assert len(all_logs["export-group"]["export-stream"]) == 2

    group_logs = core.export("export-group")
    assert len(group_logs["export-stream"]) == 2

    stream_logs = core.export("export-group", "export-stream")
    assert [e["message"] for e in stream_logs] == ["E1", "E2"]