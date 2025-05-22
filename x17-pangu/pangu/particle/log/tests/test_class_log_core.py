import time
import pytest
from unittest.mock import MagicMock

from pangu.particle.log.log_core import LogCore
from pangu.particle.log.log_group import LogGroup
from pangu.particle.log.log_event import LogEvent


def test_register_group_initializes_group_dict():
    core = LogCore(name="core1")
    group = LogGroup(name="groupA")
    
    assert group.name not in core.groups
    core.register_group(group)
    assert group.name in core.groups
    assert isinstance(core.groups[group.name], dict)
    assert group.core == core


def test_push_event_consumed_by_core():
    core = LogCore(name="core2")
    group_name = "g1"
    stream_name = "s1"
    event = LogEvent(message="Core test", name=stream_name)

    # 手动预设组结构，模拟 register
    core.groups[group_name] = {}

    core.push(group_name, stream_name, event)
    time.sleep(0.1)  # 等待消费线程处理

    assert group_name in core.groups
    assert stream_name in core.groups[group_name]
    assert core.groups[group_name][stream_name][0].message == "Core test"


def test_export_full_and_partial():
    core = LogCore(name="core3")
    g, s = "gX", "sX"
    event = LogEvent(message="Export this", name=s)
    core.groups[g] = {s: [event]}

    full = core.export()
    assert g in full and s in full[g]
    assert full[g][s][0]["message"] == "Export this"

    by_group = core.export(group=g)
    assert s in by_group
    assert by_group[s][0]["message"] == "Export this"

    by_stream = core.export(group=g, stream=s)
    assert isinstance(by_stream, list)
    assert by_stream[0]["message"] == "Export this"


def test_export_empty_is_safe():
    core = LogCore()
    assert core.export() == {}


def test_multiple_groups_and_streams():
    core = LogCore()
    group1 = "g1"
    group2 = "g2"
    event1 = LogEvent(message="log1", name="s1")
    event2 = LogEvent(message="log2", name="s2")

    core.groups[group1] = {"s1": [event1]}
    core.groups[group2] = {"s2": [event2]}

    export = core.export()
    assert export[group1]["s1"][0]["message"] == "log1"
    assert export[group2]["s2"][0]["message"] == "log2"