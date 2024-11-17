from moto.particle.text import text
import hashlib
import pytest # type: ignore

@pytest.fixture
def sample_text():
	return text("Hey there! How are you?")

def test_class(sample_text):
	assert sample_text.content == "Hey there! How are you?"


def test_instance_to_digest(sample_text):
	sample_hash = text(hashlib.sha256("Hey there! How are you?".encode()).hexdigest())
	assert sample_text.to_digest(algorithm = "sha256",) == sample_hash

def test_instance_as_digest(sample_text):
	sample_text.as_digest(algorithm = "sha256")
	sample_hash = text('24a1abfc554fea61a127b88d8e3206183c0154ae0fa976d31d975e59fd269e97')
	assert sample_text == sample_hash
