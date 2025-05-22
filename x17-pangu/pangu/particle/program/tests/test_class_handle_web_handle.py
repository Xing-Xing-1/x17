import pytest
from pangu.particle.program.handle.web import WebHandle

@pytest.fixture
def web_handle():
    return WebHandle(url="https://httpbin.org")

def test_is_available(web_handle):
    assert web_handle.is_available() is True

def test_get_root(web_handle):
    resp = web_handle.get("/")
    assert resp.code in [200, 404]
    assert isinstance(resp.text, str)

def test_post_invalid(web_handle):
    resp = web_handle.post("/", body={"invalid": True})
    assert resp.code >= 400

def test_get_tags(web_handle):
    resp = web_handle.get("/api/tags")
    assert isinstance(resp.code, int)
    assert resp.code in [200, 404]
    
    