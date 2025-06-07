# -*- coding: utf-8 -*-
import pytest
from types import SimpleNamespace
from typing import Dict, Any
import time

from x17_base.particle.log import LogGroup
from x17_base.particle.log import LogStream
from x17_intelligence.handler.base import BaseHandler


class MockHandler(BaseHandler):
    def require_env(self) -> Dict[str, Any]:
        self.log("Env check passed", level="info", context="env-check", code=200)
        return {"env_ready": True}


@pytest.fixture
def mock_interface():
    return SimpleNamespace(
        log_group=LogGroup(name="TestGroup", sync=True),
    )

def test_handler_log_basic(mock_interface):
    handler = MockHandler(name="TestHandler", interface=mock_interface)
    handler.log("Test message", level="info", context="test-case", code=100)
    export = mock_interface.log_group.export()
    assert "TestHandlerLogStream" in export
    events = export["TestHandlerLogStream"]
    assert any("Test message" in e["message"] for e in events)
    assert any(e["context"] == "test-case" for e in events)
    assert any(e["code"] == 100 for e in events)


def test_handler_require_env(mock_interface):
    handler = MockHandler(name="TestHandler", interface=mock_interface)
    result = handler.require_env()
    assert result["env_ready"] is True
    export = mock_interface.log_group.export()
    messages = [e["message"] for e in export["TestHandlerLogStream"]]
    assert "Env check passed" in messages

