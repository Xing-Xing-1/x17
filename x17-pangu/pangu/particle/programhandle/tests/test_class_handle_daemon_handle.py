import time
import pytest
from pangu.particle.programhandle.daemon import DaemonHandle
from pangu.particle.terminal.command import Command

@pytest.fixture
def http_server_daemon():
    daemon = DaemonHandle.from_name(
        name="http.server",
        start_command="python3 -m http.server 8000",
        stop_command="pkill -f 'python3 -m http.server 8000'"
    )
    yield daemon
    daemon.kill()
    time.sleep(1)


def test_start(http_server_daemon):
    response = http_server_daemon.start(force=True)
    time.sleep(5)
    assert response.success
    assert http_server_daemon.is_available


def test_stop(http_server_daemon):
    http_server_daemon.start(force=True)
    time.sleep(5)
    response = http_server_daemon.stop(force=True)
    assert response.success


def test_restart(http_server_daemon):
    http_server_daemon.start(force=True)
    time.sleep(0.5)
    assert http_server_daemon.is_available

    http_server_daemon.restart(force=True)
    for _ in range(10):
        if http_server_daemon.is_available:
            break
        time.sleep(0.2)

    assert http_server_daemon.is_available


def test_kill(http_server_daemon):
    http_server_daemon.start(force=True)
    time.sleep(0.5)
    assert http_server_daemon.is_available
    killed = http_server_daemon.kill()
    assert isinstance(killed, set)
    assert not http_server_daemon.is_available


def test_clear(http_server_daemon):
    http_server_daemon.start(force=True)
    time.sleep(0.5)
    http_server_daemon.clear()
    assert all(p.is_alive for p in http_server_daemon.internal_processes)


def test_bool(http_server_daemon):
    http_server_daemon.start(force=True)
    time.sleep(0.5)
    assert bool(http_server_daemon) is True


def test_len(http_server_daemon):
    http_server_daemon.start(force=True)
    time.sleep(0.5)
    assert len(http_server_daemon) > 0


def test_dict(http_server_daemon):
    http_server_daemon.start(force=True)
    time.sleep(0.5)
    d = http_server_daemon.dict
    assert isinstance(d, dict)
    assert "name" in d
    assert "pids" in d


def test_repr(http_server_daemon):
    r = repr(http_server_daemon)
    assert "DaemonHandle" in r
    assert http_server_daemon.name in r


def test_get_version(http_server_daemon):
    version = http_server_daemon.get_version(option="--version")
    assert isinstance(version, str) or version is None
    
def test_start_and_status(http_server_daemon):
    response = http_server_daemon.start(force=True)
    assert response.success
    assert http_server_daemon.is_available
    assert len(http_server_daemon.spawned) >= 1

def test_restart(http_server_daemon):
    http_server_daemon.start(force=True)
    response = http_server_daemon.restart(force=True)
    assert response.success
    assert http_server_daemon.is_available

def test_kill(http_server_daemon):
    http_server_daemon.start(force=True)
    pids = http_server_daemon.kill()
    assert isinstance(pids, set)
    assert not http_server_daemon.is_available

def test_run(http_server_daemon):
    http_server_daemon.start(force=True)
    time.sleep(2)
    response = http_server_daemon.run(
        Command(cmd="curl -s http://localhost:8000", shell=True, sync=True)
    )
    assert response.success
    assert "Directory" in response.stdout or "Index of" in response.stdout

def test_repr(http_server_daemon):
    http_server_daemon.start(force=True)
    output = repr(http_server_daemon)
    assert "DaemonHandle" in output
    assert "http.server" in output

def test_version_fetch():
    handle = DaemonHandle.from_name("python3", None, None)
    version = handle.get_version()
    assert version is None or isinstance(version, str)