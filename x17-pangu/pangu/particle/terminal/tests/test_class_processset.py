from unittest.mock import MagicMock

import pytest
from pangu.particle.terminal import Process
from pangu.particle.terminal.processset import ProcessSet


def make_mock_process(**kwargs):
    mock = MagicMock(spec=Process)
    for attr in ["cmdline", "name", "username", "cwd", "exe"]:
        setattr(mock, attr, kwargs.get(attr, ""))
    mock.dict = kwargs
    return mock


@pytest.fixture
def process_set():
    processes = [
        make_mock_process(
            cmdline="python app.py",
            name="python",
            username="user1",
            cwd="/home/user1",
            exe="/usr/bin/python",
        ),
        make_mock_process(
            cmdline="nginx: worker",
            name="nginx",
            username="root",
            cwd="/",
            exe="/usr/sbin/nginx",
        ),
        make_mock_process(
            cmdline="postgres -D /var/lib/postgres",
            name="postgres",
            username="postgres",
            cwd="/var",
            exe="/usr/bin/postgres",
        ),
    ]
    return ProcessSet(processes=processes)


def test_len(process_set):
    assert len(process_set) == 3


def test_iter(process_set):
    assert all(isinstance(p, Process) for p in process_set)


def test_getitem(process_set):
    assert isinstance(process_set[0], Process)


def test_repr_str(process_set):
    assert "ProcessSet" in repr(process_set)
    assert "ProcessSet" in str(process_set)


def test_dict(process_set):
    d = process_set.dict
    assert isinstance(d, dict)
    assert "processes" in d
    assert isinstance(d["processes"], list)


def test_add_remove(process_set):
    new_proc = make_mock_process(
        pid=1234,
        cmdline="java -jar server.jar",
        name="java",
        username="user2",
    )
    process_set.add(new_proc)
    assert new_proc in process_set.processes
    process_set.remove(new_proc)
    assert new_proc not in process_set.processes


def test_sort_by(process_set):
    sorted_set = process_set.sort_by("username")
    usernames = [p.username for p in sorted_set]
    assert usernames == sorted(usernames)


def test_match_ignore_case(process_set):
    result = process_set.match(
        "python",
        ["cmdline"],
        ignore_case=True,
    )
    assert len(result) == 1


def test_match_case_sensitive(process_set):
    result = process_set.match(
        "Python",
        ["cmdline"],
        ignore_case=False,
    )
    assert len(result) == 0


def test_match_regex(process_set):
    result = process_set.match_regex(
        r"nginx.*",
        ["cmdline"],
    )
    assert len(result) == 1


def test_match_wildcard(process_set):
    result = process_set.match_wildcard(
        "postgres*",
        ["cmdline"],
    )
    assert len(result) == 1
