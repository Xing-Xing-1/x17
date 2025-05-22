import pytest
from pangu.particle.platform.platform import Platform


@pytest.fixture
def platform():
    return Platform(name="TestPlatform")


def test_basic_attributes(platform):
    assert isinstance(platform.name, str)
    assert isinstance(platform.platform, str)
    assert platform.os in ("darwin", "linux", "windows")
    assert isinstance(platform.architecture, str)
    assert isinstance(platform.python_version, str)
    assert isinstance(platform.hostname, str)
    assert isinstance(platform.env_vars, dict)


def test_ip_address(platform):
    ip = platform.ip_address
    assert isinstance(ip, str)
    assert "." in ip or ip == "127.0.0.1"


def test_is_macos_linux_windows_exclusive(platform):
    flags = [platform.is_macos, platform.is_linux, platform.is_windows]
    assert sum(flags) == 1  # Only one should be True


def test_custom_kwargs():
    p = Platform(custom_thing="hello")
    assert hasattr(p, "custom_thing")
    assert p.custom_thing == "hello"