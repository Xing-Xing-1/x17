import pytest
import docker
import tempfile
from pathlib import Path
from unittest.mock import MagicMock
from docker.client import DockerClient
from docker.models.images import Image as DockerImage
import docker

from x17_container.dockers.image.image import Image
from x17_container.dockers.image.imageaction import ImageAction
from x17_container.dockers.image.imagetype import ImageType
from x17_container.dockers.image.imagebuild import ImageBuild


# ---------- Fixtures ----------

@pytest.fixture(scope="module")
def docker_client():
    return docker.from_env()

@pytest.fixture(scope="module")
def hello_world_image_obj(docker_client):
    return docker_client.images.pull("hello-world:latest")

@pytest.fixture
def image_init_from_docker(docker_client, hello_world_image_obj):
    raw_image = Image.from_docker(
        docker_client=docker_client,
        docker_image=hello_world_image_obj,
        name="hello-world:latest",
        verbose=True,
    )
    raw_image.load_attrs()
    return raw_image

@pytest.fixture
def image_init_from_remote(docker_client, request):
    image = Image(
        docker_client=docker_client,
        name="hello-world:latest",
        remote="hello-world:latest",
        action="PULL",
        verbose=True,
    )
    return image

@pytest.fixture
def image_init_custom(docker_client, request):
    tmpdir = tempfile.TemporaryDirectory()
    dockerfile = Path(tmpdir.name) / "Dockerfile"
    dockerfile.write_text("FROM scratch\nLABEL maintainer='x17'\n")

    image = Image(
        docker_client=docker_client,
        name="x17-test-local:latest",
        build={"path": tmpdir.name, "tag": "x17-test-local:latest"},
        action="BUILD",
        verbose=True,
    )

    request.addfinalizer(lambda: (tmpdir.cleanup()))
    return image

@pytest.fixture
def image_init_hybrid(docker_client, request):
    tmpdir = tempfile.TemporaryDirectory()
    dockerfile = Path(tmpdir.name) / "Dockerfile"
    dockerfile.write_text("FROM hello-world:latest\nLABEL maintainer='x17'\n")

    image = Image(
        docker_client=docker_client,
        name="x17-hybrid-test:latest",
        remote="hello-world:latest",
        build={"path": tmpdir.name, "tag": "x17-hybrid-test:latest"},
        action="PULL_BUILD",
        verbose=True,
    )

    request.addfinalizer(lambda: (tmpdir.cleanup()))
    return image

@pytest.fixture
def image_init_from_dict(docker_client, request):
    data = {
        "name": "hello-world:latest",
        "remote": "hello-world:latest",
        "action": "PULL",
        "tags": ["hello-world:latest"]
    }
    image = Image.from_dict(
        docker_client=docker_client,
        data=data,
        verbose=True,
    )
    return image

# ---------- Helper ----------

def safe_delete(image: Image):
    try:
        image.delete(force=True)
    except Exception:
        pass

# ---------- Parametrized Tests ----------

@pytest.mark.parametrize("fixture_name", [
    "image_init_from_docker",
    "image_init_from_remote",
    "image_init_custom",
    "image_init_hybrid",
    "image_init_from_dict",
])
def test_image_should_exist_and_have_id(request, fixture_name):
    image = request.getfixturevalue(fixture_name)
    assert image.exists()
    assert image.docker_image is not None
    assert image.id is not None
    assert isinstance(image.dict, dict)
    

@pytest.mark.parametrize("fixture_name", [
    "image_init_from_remote",
    "image_init_custom",
    "image_init_hybrid",
])
def test_image_delete_and_not_exist(request, fixture_name):
    image = request.getfixturevalue(fixture_name)
    assert image.exists()
    image.delete(force=True)
    assert not image.exists()

@pytest.mark.parametrize("fixture_name,expected_type", [
    ("image_init_from_docker", ImageType.LOADED),
    ("image_init_from_remote", ImageType.SINGLETON),
    ("image_init_custom", ImageType.CUSTOM),
    ("image_init_hybrid", ImageType.HYBRID),
    ("image_init_from_dict", ImageType.SINGLETON),
])
def test_image_properties_all(request, fixture_name, expected_type):
    image = request.getfixturevalue(fixture_name)

    # status
    assert image.status in {"AVAILABLE", "NOT_FOUND"}

    # full_status
    full = image.full_status
    assert full.startswith("[")
    assert "]" in full
    assert image.name in full or (image.id and image.id in full)

    # image_type
    assert image.image_type == expected_type

    d = image.dict
    assert isinstance(d, dict)
    assert d["name"] == image.name
    assert d["image_type"] == expected_type
    assert d["status"] == image.status
    assert d["full_status"] == full

    # str/repr
    s = str(image)
    r = repr(image)
    assert isinstance(s, str)
    assert isinstance(r, str)
    assert image.name in s or (image.id and image.id in s)
    assert image.name in r or (image.id and image.id in r)
    
@pytest.fixture
def mock_docker_image():
    mock = MagicMock(spec=DockerImage)
    mock.id = "sha256:abc123"
    mock.labels = {"maintainer": "x17"}
    mock.tags = ["custom-image:latest"]
    mock.attrs = {
        "RepoTags": ["custom-image:latest"],
        "RepoDigests": ["custom-image@sha256:def456"],
        "Parent": "parent-image",
        "Comment": "This is a test image",
        "Created": "2025-06-18T10:00:00.000Z",
        "DockerVersion": "20.10.5",
        "Author": "x17",
        "Config": {"Env": ["VAR=1"]},
        "Architecture": "amd64",
        "Variant": None,
        "Os": "linux",
        "Size": 123456,
        "GraphDriver": {"Name": "overlay2"},
        "RootFS": {"Type": "layers"},
        "Metadata": {"LastTagTime": "2025-06-18T10:00:00.000Z"},
        "Descriptor": {"mediaType": "application/vnd.docker.distribution.manifest.v2+json"},
    }
    return mock

def test_load_attrs(mock_docker_image):
    image = Image(
        docker_client=MagicMock(spec=DockerClient),
        docker_image=mock_docker_image,
        action=ImageAction("MANUAL"),
        name="custom-image:latest",
    )
    image.load_attrs()
    assert image.id == "sha256:abc123"
    assert image.name == "custom-image:latest"
    assert image.repotags == ["custom-image:latest"]
    assert image.repodigests == ["custom-image@sha256:def456"]
    assert image.comment == "This is a test image"
    assert image.created == "2025-06-18T10:00:00.000Z"
    assert image.docker_version == "20.10.5"
    assert image.author == "x17"
    assert image.config == {"Env": ["VAR=1"]}
    assert image.architecture == "amd64"
    assert image.os == "linux"
    assert image.size == 123456
    assert image.graph_driver == {"Name": "overlay2"}
    assert image.rootfs == {"Type": "layers"}
    assert image.metadata == {"LastTagTime": "2025-06-18T10:00:00.000Z"}
    assert image.descriptor == {"mediaType": "application/vnd.docker.distribution.manifest.v2+json"}
    
@pytest.mark.parametrize("fixture_name,expected_type", [
    ("image_init_from_remote", ImageType.SINGLETON),
    ("image_init_custom", ImageType.CUSTOM),
    ("image_init_hybrid", ImageType.HYBRID),
])
def test_load_attrs_from_fixture(request, fixture_name, expected_type):
    image = request.getfixturevalue(fixture_name)
    image.load_attrs()
    assert image.image_type == expected_type
    assert image.name
    assert isinstance(image.size, int)
    assert isinstance(image.full_status, str)
    assert image.dict["image_type"] == expected_type
    
    
@pytest.mark.parametrize("fixture_name,expected", [
    ("image_init_from_remote", True),
    ("image_init_from_dict", True),
])
def test_exists_remote_true(request, fixture_name, expected):
    image = request.getfixturevalue(fixture_name)
    assert image.exists_remote() == expected

def test_exists_remote_false(docker_client):
    image = Image(
        docker_client=docker_client,
        name="x17-nonexistent-test:latest",
        remote="x17-nonexistent-test:latest",
        action="MANUAL",
        verbose=True,
    )
    assert image.exists_remote() is False

def test_pull_no_remote_check_true(docker_client):
    image = Image(
        docker_client=docker_client,
        remote=None,
        name="x17-test-noremote",
        action="MANUAL",
        verbose=True,
    )
    with pytest.raises(ValueError):
        image.pull(force=True, check=True)


def test_pull_no_remote_check_false(docker_client):
    image = Image(
        docker_client=docker_client,
        remote=None,
        name="x17-test-noremote",
        action="MANUAL",
        verbose=True,
    )
    image.pull(force=True, check=False)
    assert image.docker_image is None


def test_pull_not_exist_check_false(docker_client):
    image = Image(
        docker_client=docker_client,
        remote="x17-nonexistent-test:latest",
        name="x17-nonexistent-test",
        action="MANUAL",
        verbose=True,
    )
    image.pull(force=True, check=False)
    assert image.docker_image is None


def test_pull_not_exist_check_true(docker_client):
    image = Image(
        docker_client=docker_client,
        remote="x17-nonexistent-test:latest",
        name="x17-nonexistent-test",
        action="MANUAL",
        verbose=True,
    )
    with pytest.raises(RuntimeError):
        image.pull(force=True, check=True)


def test_build_fail_continue(docker_client, tmp_path):
    dockerfile = tmp_path / "Dockerfile"
    dockerfile.write_text("FROM busybox\nRUN exit 1\n")
    build_config = {
        "path": str(tmp_path),
        "dockerfile": "Dockerfile",
        "tag": "x17-fake-fail",
        "rm": True,
        "quiet": False,
    }
    image = Image(
        docker_client=docker_client,
        name="x17-fake-fail",
        build=build_config,
        action="MANUAL",
        verbose=True,
    )
    image.build(check=False)
    assert image.docker_image is None


def test_build_fail_raise(docker_client, tmp_path):
    dockerfile = tmp_path / "Dockerfile"
    dockerfile.write_text("FROM busybox\nRUN exit 1\n")
    build_config = {
        "path": str(tmp_path),
        "dockerfile": "Dockerfile",
        "tag": "x17-fake-fail",
        "rm": True,
        "quiet": False,
    }
    image = Image(
        docker_client=docker_client,
        name="x17-fake-fail",
        build=build_config,
        action="MANUAL",
        verbose=True,
    )
    with pytest.raises(RuntimeError):
        image.build(check=True)
        

@pytest.mark.parametrize("tag_name", ["testtag", "newtag"])
def test_add_tag_creates_new_tag(image_init_from_remote, tag_name):
    image = image_init_from_remote
    new_image = image.add_tag(tag_name)
    assert f"{image.repository}:{tag_name}" in new_image.tags
    assert new_image.tag == tag_name
    new_image.delete_tag(tag_name)


@pytest.mark.parametrize("tag_name", ["tempdel"])
def test_delete_tag_removes_tag(image_init_from_remote, tag_name):
    image = image_init_from_remote
    image.add_tag(tag_name)
    deleted = image.delete_tag(tag_name)
    assert deleted
    
def test_image_init_with_skip(docker_client):
    docker_image = docker_client.images.pull("hello-world:latest")
    image = Image(
        docker_client=docker_client,
        docker_image=docker_image,
        name="hello-world:latest",
        skip=True,
        verbose=True,
    )
    assert image.name == "hello-world:latest"
    assert image.id is not None

def test_image_init_without_skip(docker_client):
    docker_image = docker_client.images.pull("hello-world:latest")
    image = Image(
        docker_client=docker_client,
        docker_image=docker_image,
        name="hello-world:latest",
        skip=False,
        verbose=True,
    )
    assert image.name == "hello-world:latest"
    assert image.id is not None
    
# ---------- Integration Tests ----------


client = docker.from_env()

def test_image_pull_add_and_delete_tag():
    img = Image(
        docker_client=client,
        remote="hello-world",
        name="hello-world:pytest-original",
        action=ImageAction(mode="PULL"),
        verbose=True,
    )

    assert "hello-world:pytest-original" in img.tags or "hello-world:latest" in img.tags

    new_tag = "pytest-tag"
    new_img = img.add_tag(new_tag)
    assert any(t.endswith(new_tag) for t in new_img.tags)

    deleted = new_img.delete_tag(new_tag)
    assert deleted is True

    img.delete(force=True)

def test_image_build_add_and_delete_tag(tmp_path):
    dockerfile = tmp_path / "Dockerfile"
    dockerfile.write_text("FROM hello-world")

    build_conf = ImageBuild({
        "path": str(tmp_path),
        "dockerfile": "Dockerfile",
        "tag": "pytest-build:latest",
        "rm": True,
    })

    img = Image(
        docker_client=client,
        build=build_conf,
        name="pytest-build:latest",
        action=ImageAction(mode="BUILD"),
        verbose=True,
    )

    assert "pytest-build:latest" in img.tags

    new_tag = "backup"
    img2 = img.add_tag(new_tag)
    assert any(t.endswith(new_tag) for t in img2.tags)

    img2.delete_tag(new_tag)
    img.delete(force=True)
    img2.delete(force=True)
    
# ---------- Cleanup ----------
    
def pytest_sessionfinish(session, exitstatus):
    client = docker.from_env()
    images_to_clean = [
        "hello-world:latest",
        "x17-test-local:latest",
        "x17-hybrid-test:latest",
        "pytest-build:latest",
    ]
    for image_name in images_to_clean:
        try:
            client.images.remove(image_name, force=True)
            print(f"✅ Removed leftover image: {image_name}")
        except docker.errors.ImageNotFound:
            pass
        except Exception as e:
            print(f"⚠️ Failed to delete {image_name}: {e}")
            
            