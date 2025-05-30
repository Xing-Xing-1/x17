import os
import subprocess
import time
from unittest.mock import MagicMock, patch

import psutil
import pytest
from pangu.particle.terminal.process import Process


def test_process_basic_info():
    current_pid = os.getpid()
    proc = Process.from_pid(current_pid)
    assert proc is not None
    assert proc.pid == current_pid
    assert proc.name != ""
    assert isinstance(proc.dict, dict)
    assert proc.is_running
    assert proc.cpu_percent >= 0.0
    assert proc.memory_percent >= 0.0


@patch("pangu.particle.terminal.process.PsutilProcess")
def test_kill_is_safe(mock_psutil):
    mock_proc = MagicMock()
    mock_proc.kill.return_value = True
    mock_proc.pid = os.getpid()
    mock_psutil.return_value = mock_proc

    proc = Process(proc=mock_proc)
    assert proc.kill() is True
    mock_proc.kill.assert_called_once()


def test_create_from_pid():
    pid = os.getpid()
    proc = Process.from_pid(pid)
    assert proc is not None
    assert proc.pid == pid
    assert proc.name != ""
    assert isinstance(proc.cmdline, str)


def test_create_from_object():
    ps_proc = psutil.Process(os.getpid())
    proc = Process.from_object(ps_proc)
    assert proc is not None
    assert proc.pid == ps_proc.pid
    assert proc.username != ""


def test_basic_attributes():
    proc = Process.from_pid(os.getpid())
    assert isinstance(proc.memory_percent, float)
    assert proc.status in ["running", "sleeping", "idle", "unknown"]


def test_memory_info():
    proc = Process.from_pid(os.getpid())
    mem_info = proc.memory_info
    assert isinstance(mem_info, dict)
    assert "rss" in mem_info


def test_cpu_times():
    proc = Process.from_pid(os.getpid())
    cpu_times = proc.get_cpu_times()
    assert isinstance(cpu_times, dict)
    assert "user" in cpu_times


def test_open_files_safe():
    proc = Process.from_pid(os.getpid())
    files = proc.get_open_files()
    assert isinstance(files, dict)


def test_threads_safe():
    proc = Process.from_pid(os.getpid())
    threads = proc.get_threads()
    assert isinstance(threads, list)
    if threads:
        assert "id" in threads[0]


def test_connections_safe():
    proc = Process.from_pid(os.getpid())
    conns = proc.get_connections()
    assert isinstance(conns, list)


def test_children_safe():
    proc = Process.from_pid(os.getpid())
    children = proc.get_children()
    assert isinstance(children, list)


def test_state_flags():
    proc = Process.from_pid(os.getpid())
    _ = proc.is_zombie
    _ = proc.is_running
    _ = proc.is_root
    _ = proc.is_system


@pytest.fixture(scope="function")
def dummy_process():
    proc = subprocess.Popen(["sleep", "10"])
    yield proc
    proc.kill()
    


def test_kill(dummy_process):
    proc = Process.from_pid(dummy_process.pid)
    assert proc is not None
    assert proc.is_running
    success = proc.kill()
    assert success is True

    proc.wait(timeout=2)
    assert not proc.is_running


def test_terminate(dummy_process):
    proc = Process.from_pid(dummy_process.pid)
    assert proc is not None
    assert proc.is_running
    success = proc.terminate()
    assert success is True

    proc.wait(timeout=2)
    assert not proc.is_running


def test_suspend_resume(dummy_process):
    proc = Process.from_pid(dummy_process.pid)
    assert proc is not None
    suspend_success = proc.suspend()
    assert suspend_success is True
    time.sleep(0.5)
    resume_success = proc.resume()
    assert resume_success is True


def test_wait(dummy_process):
    proc = Process.from_pid(dummy_process.pid)
    assert proc is not None
    dummy_process.terminate()
    exited = proc.wait(timeout=3)
    assert exited is not None
