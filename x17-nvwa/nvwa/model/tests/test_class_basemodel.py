import pytest
import time

from nvwa.model.base import BaseModel
from pangu.particle.log import LogGroup


class DummyInterface:
    def __init__(self):
        self.log_group = LogGroup(name="DummyInterfaceLogGroup", sync_mode=True)


def test_base_model_log():
    log_group = LogGroup(name="DummyInterfaceLogGroup", sync_mode=True)
    interface = DummyInterface()
    interface.log_group = log_group
    model = BaseModel(name="test-model", interface=interface)
    log_group.register_stream(model.log_stream)
    model.log("Model init successful", context="startup", code=200)
    logs = log_group.export()
    log_entries = logs.get(model.log_stream.name, [])

    assert any(
        log["message"] == "Model init successful" and log["context"] == "startup"
        for log in log_entries
    )


def test_model_ready_flag_mutable():
    model = BaseModel(name="readiness")
    assert model.ready is False
    model.ready = True
    assert model.ready is True


def test_model_log_without_interface():
    model = BaseModel(name="no-interface")
    log_group = LogGroup(name="NoInterfaceLogGroup", sync_mode=True)
    model.log_stream.group = log_group
    log_group.register_stream(model.log_stream)
    model.log("No interface test", context="bare")
    logs = log_group.export()[model.log_stream.name]
    assert any(log["message"] == "No interface test" for log in logs)


def test_model_custom_log_stream():
    custom_group = LogGroup(name="CustomGroup", sync_mode=True)
    from pangu.particle.log import LogStream

    custom_stream = LogStream(name="CustomStream", group=custom_group)
    model = BaseModel(name="custom", log_stream=custom_stream)
    custom_group.register_stream(custom_stream)
    model.log("Using custom stream", context="custom")
    logs = custom_group.export()["CustomStream"]
    assert any("custom stream" in log["message"].lower() for log in logs)
