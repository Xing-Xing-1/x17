from moto.particle.base.file import File
from moto.particle.datestamp import datestamp
import pytest # type: ignore
import os # type: ignore

cwd = os.getcwd()

@pytest.fixture
def empty_file():
	return File()

@pytest.fixture
def sample_file():
	path = "tests/env/sample.txt"
	return File(path = path)

def test_init_default(empty_file):
	assert empty_file.path == None
	assert empty_file.full_path == None
	assert empty_file.name == None
	assert empty_file.extension == None
	assert empty_file.exists == False
	assert empty_file.created_at == empty_file.updated_at

def test_init_with_path(sample_file):
	assert sample_file.full_path.as_posix() == f"{cwd}/tests/env/sample.txt"
	assert sample_file.path.as_posix() == "tests/env/sample.txt"
	assert sample_file.name == 'sample.txt'
	assert sample_file.suffix == '.txt'
	assert sample_file.exists == True
	assert sample_file.created_at == sample_file.updated_at

def test_set(empty_file):
	path = "tests/env/sample.txt"
	empty_file.set(path = path)
	assert empty_file.full_path.as_posix() == f"{cwd}/tests/env/sample.txt"
	assert empty_file.path.as_posix() == "tests/env/sample.txt"
	assert empty_file.name == 'sample.txt'
	assert empty_file.suffix == '.txt'
	assert empty_file.exists == True
	assert empty_file.created_at == empty_file.updated_at

def test_get_attributes(sample_file):
	assert sample_file.get_name() == 'sample.txt'
	assert sample_file.get_path() == sample_file.path
	assert sample_file.get_fullpath() == sample_file.full_path 
	assert sample_file.get_suffix() == '.txt'
	
	assert sample_file.get_path(as_str = True) == "tests/env/sample.txt"
	assert sample_file.get_fullpath(as_str = True) == f"{cwd}/tests/env/sample.txt"

def test_get_empty_attributes(empty_file):
	assert empty_file.get_name() == None
	assert empty_file.get_path() == None
	assert empty_file.get_fullpath() == None
	assert empty_file.get_suffix() == None

def test_exists(sample_file):
	assert sample_file.exists == True

def test_not_exists(empty_file):
	assert empty_file.exists == False

def test_not_exists_after_set(empty_file):
	path = "tests/env/sample.txt"
	empty_file.set(path = path)
	assert empty_file.exists == True
	empty_file.set(path = "tests/env/sample2.txt")
	assert empty_file.exists == False
	empty_file.set(path = path)
	assert empty_file.exists == True

def test_update_datestamp(empty_file):
	empty_file.update_datestamp()
	assert empty_file.updated_at != empty_file.created_at
	assert empty_file.updated_at != None
	assert empty_file.created_at != None
	assert empty_file.updated_at < empty_file.created_at

def test_update_datestamp_with_datestamp(empty_file):
	empty_file.update_datestamp(
		updated_at = datestamp.from_str(
			"2021-01-01", 
			datestamp_format='%Y-%m-%d'),
		)
	assert empty_file.updated_at == datestamp.from_str(
		"2021-01-01", 
		datestamp_format='%Y-%m-%d',
	)
	assert empty_file.created_at != empty_file.updated_at
	assert empty_file.created_at != None
	assert empty_file.updated_at != None