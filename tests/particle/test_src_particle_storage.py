from moto.particle.storage import storage
import pytest # type: ignore

@pytest.fixture
def storage_sample_map():
	return {
		"b": storage(500, "b"),
		"kb": storage(500, "kb"),
		"mb": storage(500, "mb"),
		"gb": storage(500, "gb"),
		"tb": storage(500, "tb"),
		"pb": storage(500, "pb"),
	}

def test_class(storage_sample_map):
	assert storage_sample_map["b"].size == 500
	assert storage_sample_map["b"].unit == "b"
	assert storage_sample_map["kb"].size == 500
	assert storage_sample_map["kb"].unit == "kb"
	assert storage_sample_map["mb"].size == 500
	assert storage_sample_map["mb"].unit == "mb"
	assert storage_sample_map["gb"].size == 500
	assert storage_sample_map["gb"].unit == "gb"
	assert storage_sample_map["tb"].size == 500
	assert storage_sample_map["tb"].unit == "tb"
	assert storage_sample_map["pb"].size == 500
	assert storage_sample_map["pb"].unit == "pb"

def test_class_str(storage_sample_map):
	assert str(storage_sample_map["b"]) == "500 b"
	assert str(storage_sample_map["kb"]) == "500 kb"
	assert str(storage_sample_map["mb"]) == "500 mb"
	assert str(storage_sample_map["gb"]) == "500 gb"
	assert str(storage_sample_map["tb"]) == "500 tb"
	assert str(storage_sample_map["pb"]) == "500 pb"

def test_class_eq(storage_sample_map):
	assert storage_sample_map["b"] == storage(500, "b")
	assert storage_sample_map["kb"] == storage(500, "kb")
	assert storage_sample_map["mb"] == storage(500, "mb")
	assert storage_sample_map["gb"] == storage(500, "gb")
	assert storage_sample_map["tb"] == storage(500, "tb")
	assert storage_sample_map["pb"] == storage(500, "pb")

def test_class_ne(storage_sample_map):
	assert storage_sample_map["b"] != storage(500, "kb")
	assert storage_sample_map["kb"] != storage(500, "mb")
	assert storage_sample_map["mb"] != storage(500, "gb")
	assert storage_sample_map["gb"] != storage(500, "tb")
	assert storage_sample_map["tb"] != storage(500, "pb")
	assert storage_sample_map["pb"] != storage(500, "b")

def test_class_add(storage_sample_map):
	assert storage_sample_map["b"] + storage(500, "b") == storage(1000, "b")
	assert storage_sample_map["kb"] + storage(500, "kb") == storage(1000, "kb")
	assert storage_sample_map["mb"] + storage(500, "mb") == storage(1000, "mb")
	assert storage_sample_map["gb"] + storage(500, "gb") == storage(1000, "gb")
	assert storage_sample_map["tb"] + storage(500, "tb") == storage(1000, "tb")
	assert storage_sample_map["pb"] + storage(500, "pb") == storage(1000, "pb")
	assert storage_sample_map["b"] + storage(1, "kb") == storage(1524, "b")
	assert storage_sample_map["kb"] + storage(1, "mb") == storage(1524, "kb")
	assert storage_sample_map["mb"] + storage(1, "gb") == storage(1524, "mb")
	assert storage_sample_map["gb"] + storage(1, "tb") == storage(1524, "gb")
	assert storage_sample_map["tb"] + storage(1, "pb") == storage(1524, "tb")
	
def test_class_sub(storage_sample_map):
	assert storage_sample_map["b"] - storage(500, "b") == storage(0, "b")
	assert storage_sample_map["kb"] - storage(500, "kb") == storage(0, "kb")
	assert storage_sample_map["mb"] - storage(500, "mb") == storage(0, "mb")
	assert storage_sample_map["gb"] - storage(500, "gb") == storage(0, "gb")
	assert storage_sample_map["tb"] - storage(500, "tb") == storage(0, "tb")
	assert storage_sample_map["pb"] - storage(500, "pb") == storage(0, "pb")
	assert storage_sample_map["b"] - storage(1, "kb") == storage(-524, "b")
	assert storage_sample_map["kb"] - storage(1, "mb") == storage(-524, "kb")
	assert storage_sample_map["mb"] - storage(1, "gb") == storage(-524, "mb")
	assert storage_sample_map["gb"] - storage(1, "tb") == storage(-524, "gb")
	assert storage_sample_map["tb"] - storage(1, "pb") == storage(-524, "tb")

def test_class_mul(storage_sample_map):
	assert storage_sample_map["b"] * 2 == storage(1000, "b")
	assert storage_sample_map["kb"] * 2 == storage(1000, "kb")
	assert storage_sample_map["mb"] * 2 == storage(1000, "mb")
	assert storage_sample_map["gb"] * 2 == storage(1000, "gb")
	assert storage_sample_map["tb"] * 2 == storage(1000, "tb")
	assert storage_sample_map["pb"] * 2 == storage(1000, "pb")
	assert storage_sample_map["b"] * 1024 == storage(512000, "b")
	assert storage_sample_map["kb"] * 1024 == storage(512000, "kb")
	assert storage_sample_map["mb"] * 1024 == storage(512000, "mb")
	assert storage_sample_map["gb"] * 1024 == storage(512000, "gb")
	assert storage_sample_map["tb"] * 1024 == storage(512000, "tb")
	assert storage_sample_map["pb"] * 1024 == storage(512000, "pb")

def test_class_to_unit(storage_sample_map):
	assert storage_sample_map["b"].to_unit("b") == storage(500, "b")
	assert storage_sample_map["kb"].to_unit("kb") == storage(500, "kb")
	assert storage_sample_map["mb"].to_unit("mb") == storage(500, "mb")
	assert storage_sample_map["gb"].to_unit("gb") == storage(500, "gb")
	assert storage_sample_map["tb"].to_unit("tb") == storage(500, "tb")
	assert storage_sample_map["pb"].to_unit("pb") == storage(500, "pb")
	assert storage_sample_map["b"].to_unit("kb") == storage(0.48828125, "kb")
	assert storage_sample_map["kb"].to_unit("mb") == storage(0.48828125, "mb")
	assert storage_sample_map["mb"].to_unit("gb") == storage(0.48828125, "gb")
	assert storage_sample_map["gb"].to_unit("tb") == storage(0.48828125, "tb")
	assert storage_sample_map["tb"].to_unit("pb") == storage(0.48828125, "pb")
	assert storage_sample_map["pb"].to_unit("tb") == storage(512000, "tb")
	assert storage_sample_map["tb"].to_unit("gb") == storage(512000, "gb")
	assert storage_sample_map["gb"].to_unit("mb") == storage(512000, "mb")
	assert storage_sample_map["mb"].to_unit("kb") == storage(512000, "kb")
	assert storage_sample_map["kb"].to_unit("b") == storage(512000, "b")

