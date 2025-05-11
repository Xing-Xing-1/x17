import pytest
import time

from nvwa.interface.base import BaseInterface
from nvwa.handler.base import BaseHandler
from pangu.particle.log import LogGroup, LogStream


@pytest.fixture
def test_interface():
    """
    Fixture to create a test interface.
    """
    log_group = LogGroup(name="TestLogGroup")
    interface = BaseInterface(
        name="TestInterface",
        log_group=log_group,
    )
    return interface

def test_interface_basic_log(test_interface):
    log_group_instance = test_interface.log_group
    base_interface_instance = test_interface
    
    assert base_interface_instance.log_group is not None
    assert base_interface_instance.handler.log_stream is not None
    assert base_interface_instance.handler.log_stream.group == base_interface_instance.log_group


    base_interface_instance.log_stream.log(
        message="Test log message",
        level="info",
        context="test_context",
        code=200,
        tags=["test", "log"],
        metrics={"key": "value"},
    )
    time.sleep(0.1)
    
    logs_by_stream = base_interface_instance.log_group.export()
    stream_logs = logs_by_stream.get("TestInterfaceLogStream", [])
    assert any(
        log["message"] == "Test log message" and log["context"] == "test_context"
        for log in stream_logs
    )
    
def test_interface_log_method(test_interface):
    test_interface.log("Log via interface", context="method-test")
    time.sleep(0.1)
    logs = test_interface.log_group.export().get("TestInterfaceLogStream", [])
    assert any(
        log["message"] == "Log via interface" and log["context"] == "method-test"
        for log in logs
    )