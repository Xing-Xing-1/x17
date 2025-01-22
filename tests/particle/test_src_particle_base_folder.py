#!/usr/bin/python
# -*- coding: utf-8 -*-

from moto.particle.base.folder import BaseFolder
from moto.particle.storage import storage  # type: ignore

import pytest  # type: ignore
import os  # type: ignore

cwd = os.getcwd()


@pytest.fixture
def remote_folder_instance():
    return BaseFolder()

@pytest.fixture
def sample_folder_instance():
    test_env_path = "tests/env/"
    return BaseFolder(path = test_env_path)



def test_remote_folder_instance(remote_folder_instance):
    assert remote_folder_instance.path is None
    assert remote_folder_instance.full_path is None
    assert remote_folder_instance.name is None
    assert remote_folder_instance.exists is False

def test_sample_folder_instance(sample_folder_instance):
    assert sample_folder_instance.path is not None
    assert sample_folder_instance.full_path is not None
    assert sample_folder_instance.name is not None
    assert sample_folder_instance.exists is True

def test_remote_folder_set(remote_folder_instance):
    test_env_path = "tests/env/sample_folder/"
    remote_folder_instance.set(test_env_path)
    assert remote_folder_instance.path is not None
    assert remote_folder_instance.full_path is not None
    assert remote_folder_instance.name is not None
    assert remote_folder_instance.exists is True

def test_sample_folder_set(sample_folder_instance):
    test_env_path = "tests/env/"
    sample_folder_instance.set(test_env_path)
    assert sample_folder_instance.path is not None
    assert sample_folder_instance.full_path is not None
    assert sample_folder_instance.name is not None
    assert sample_folder_instance.exists is True


