import pytest
from unittest.mock import MagicMock
from pangu.particle.remote.call import Call
from pangu.particle.remote.url import Url
from pangu.particle.remote.response import Response
from pangu.particle.programhandle.web import WebHandle


@pytest.fixture
def sample_url():
    return Url.from_str("http://localhost:9999")


@pytest.fixture
def web_handle(sample_url):
    return WebHandle.from_name(name="mock_web", url=sample_url)


def test_basic_properties(web_handle):
    assert web_handle.name == "mock_web"
    assert str(web_handle.url) == "http://localhost:9999"
    assert isinstance(web_handle.dict, dict)
    assert "name" in web_handle.dict
    assert "url" in web_handle.dict


def test_bool_and_len(monkeypatch, web_handle):
    monkeypatch.setattr(Call, "send", lambda self: Response(code=200))
    assert bool(web_handle) is True
    assert len(web_handle) == 1


def test_run_method(monkeypatch, web_handle):
    mock_call = MagicMock(spec=Call)
    mock_call.send.return_value = Response(code=200, stdout="ok")
    result = web_handle.run(mock_call)
    assert result.code == 200


def test_get_method(monkeypatch, web_handle):
    monkeypatch.setattr(Call, "send", lambda self: Response(code=200, stdout="hello"))
    result = web_handle.get(path="/test")
    assert result.code == 200
    assert "hello" in result.stdout


def test_post_method(monkeypatch, web_handle):
    monkeypatch.setattr(Call, "send", lambda self: Response(code=201, stdout="posted"))
    result = web_handle.post(path="/submit", body={"foo": "bar"})
    assert result.code == 201
    assert "posted" in result.stdout


def test_get_version(web_handle):
    assert web_handle.get_version() == "Not supported"


def test_register_and_get_registered(web_handle):
    mock_call = MagicMock(spec=Call)
    web_handle.register("ping", mock_call)
    assert web_handle.get_registered("ping") is mock_call


def test_register_as_method(monkeypatch, web_handle):
    monkeypatch.setattr(Call, "send", lambda self: Response(code=200, stdout="pong"))
    call = Call(method="GET", url=web_handle.url)
    web_handle.register("ping", call, as_method=True)
    assert hasattr(web_handle, "ping")
    assert callable(web_handle.ping)
    resp = web_handle.ping()
    assert resp.code == 200
    assert "pong" in resp.stdout