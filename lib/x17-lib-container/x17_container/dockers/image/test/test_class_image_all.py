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
from x17_container.dockers.image.imagemeta import ImageMeta

# --------- Fixtures for Docker Client and Image Creation ---------

@pytest.fixture(scope="module")
def docker_client():
    client = docker.from_env()
    yield client
    client.close()

@pytest.fixture(scope="module")
def pull_image(docker_client):
    repo = "hello-world"
    tag = "latest"
    image = Image(
        docker_client=docker_client,
        repository=repo,
        tag=tag,
        action=ImageAction("PULL"),
    )
    yield image
    image.delete(force=True, check=False)

@pytest.fixture(scope="module")
def build_image(docker_client):
    tempdir = tempfile.TemporaryDirectory()
    dockerfile_path = Path(tempdir.name) / "Dockerfile"
    dockerfile_path.write_text("FROM alpine\nCMD echo 'hello from build'\n")
    buildparam = ImageBuild(
        path=tempdir.name, 
        dockerfile="Dockerfile", 
        tag="test-build:latest",
    )
    image = Image(
        docker_client=docker_client,
        repository="test-build",
        tag="latest",
        buildparam=buildparam,
        action=ImageAction("BUILD"),
    )
    yield image
    image.delete(force=True, check=False)
    tempdir.cleanup()
    
@pytest.fixture(scope="module")
def manual_image(docker_client):
    image = Image(
        docker_client=docker_client,
        repository="manual-test",
        tag="v1",
        action=ImageAction("MANUAL"),
    )
    yield image
    image.delete(force=True, check=False)
    
@pytest.fixture(scope="module")
def image_from_docker(docker_client):
    docker_image = docker_client.images.pull("hello-world:latest")
    image = Image.from_docker(
        docker_image=docker_image,
        docker_client=docker_client,
    )

    yield image

    try:
        docker_client.images.remove(image.name, force=True)
    except docker.errors.ImageNotFound:
        pass
    
@pytest.fixture(scope="module")
def image_from_dict(docker_client):
    base_image = Image(
        docker_client=docker_client,
        repository="hello-world",
        tag="latest",
        action=ImageAction("PULL"),
    )
    data = base_image.export()
    image = Image.from_dict(
        data, 
        docker_client=docker_client,
    )
    yield image

    try:
        image.delete(force=True, check=False)
    except Exception:
        pass



@pytest.mark.parametrize(
    "image_fixture,expected_action,expected_type",
    [
        ("pull_image", "PULL", ImageType.PULL),
        ("build_image", "BUILD", ImageType.BUILD),
        ("manual_image", "MANUAL", ImageType.MANUAL),
        ("image_from_docker", "MANUAL", ImageType.MANUAL),
        ("image_from_dict", "PULL", ImageType.PULL),
    ],
)
def test_image_properties(image_fixture, expected_action, expected_type, request):
    image = request.getfixturevalue(image_fixture)
    assert image.name == f"{image.repository}:{image.tag}"
    assert str(image.action) == expected_action
    assert image.type == expected_type
    assert image.status == "AVAILABLE" or "NOT_AVAILABLE"
    assert image.full_status.startswith("[")
    assert "AVAILABLE" in image.full_status or "NOT_AVAILABLE" in image.full_status
    assert str(image) == image.name
    assert "Image(name=" in repr(image)
    
    exported = image.dict
    assert "name" in exported
    assert "status" in exported
    assert "buildparam" in exported
    if expected_action == "BUILD":
        assert len(image.dockerlines) > 0
        assert any("FROM" in line for line in image.dockerlines)
        assert isinstance(image.cascades, list)
        assert len(image.cascades) >= 1
    else:
        assert isinstance(image.dockerlines, list)
        assert isinstance(image.cascades, list)
        
@pytest.mark.parametrize(
    "image_fixture,expected_action,expected_type",
    [
        ("pull_image", "PULL", ImageType.PULL),
        ("build_image", "BUILD", ImageType.BUILD),
        ("manual_image", "MANUAL", ImageType.MANUAL),
        ("image_from_docker", "MANUAL", ImageType.MANUAL),
        ("image_from_dict", "PULL", ImageType.PULL),
    ],
)
def test_dockerlines_and_cascades_from_build_image(image_fixture, expected_action, expected_type, request):
    build_image = request.getfixturevalue(image_fixture)
    if expected_type == ImageType.BUILD:
        lines = build_image.dockerlines
        assert isinstance(lines, list)
        assert any("FROM" in line for line in lines)
        cascades = build_image.cascades
        assert isinstance(cascades, list)
        assert any(isinstance(cascade, str) for cascade in cascades)
    else:
        assert build_image.dockerlines == []
        assert build_image.cascades == []
    
@pytest.mark.parametrize(
    "image_fixture,expected_action,expected_type",
    [
        ("pull_image", "PULL", ImageType.PULL),
        ("build_image", "BUILD", ImageType.BUILD),
        ("manual_image", "MANUAL", ImageType.MANUAL),
        ("image_from_docker", "MANUAL", ImageType.MANUAL),
        ("image_from_dict", "PULL", ImageType.PULL),
    ],
)
def test_dict_from_build_image(image_fixture, expected_action, expected_type, request):
    build_image = request.getfixturevalue(image_fixture)
    buile_image_dict = build_image.dict
    assert isinstance(buile_image_dict, dict)
    assert "id" in buile_image_dict
    assert "name" in buile_image_dict and buile_image_dict["name"] == f"{build_image.repository}:{build_image.tag}"
    assert "repository" in buile_image_dict
    assert "tag" in buile_image_dict
    assert "action" in buile_image_dict
    assert buile_image_dict["action"] == str(expected_action)
    assert "type" in buile_image_dict
    assert buile_image_dict["type"] == str(expected_type)
    assert "status" in buile_image_dict
    assert "full_status" in buile_image_dict
    assert "cascades" in buile_image_dict
    assert isinstance(buile_image_dict["cascades"], list)
    assert "buildparam" in buile_image_dict
    if expected_action == "BUILD":
        assert buile_image_dict["buildparam"] is not None
        assert isinstance(buile_image_dict["buildparam"], dict)
    assert "labels" in buile_image_dict
    assert "tags" in buile_image_dict
    assert isinstance(buile_image_dict["tags"], list)
    assert "repotags" in buile_image_dict
    assert "repodigests" in buile_image_dict
    assert "parent" in buile_image_dict
    assert "comment" in buile_image_dict
    assert "created" in buile_image_dict
    assert "docker_version" in buile_image_dict
    assert "author" in buile_image_dict
    assert "config" in buile_image_dict
    assert isinstance(buile_image_dict["config"], dict)
    assert "architecture" in buile_image_dict
    assert "variant" in buile_image_dict
    assert "os" in buile_image_dict
    assert "size" in buile_image_dict
    assert "graph_driver" in buile_image_dict
    assert "rootfs" in buile_image_dict
    assert "metadata" in buile_image_dict
    assert "descriptor" in buile_image_dict

@pytest.mark.parametrize(
    "image_fixture,expected_action,expected_type",
    [
        ("pull_image", "PULL", ImageType.PULL),
        ("build_image", "BUILD", ImageType.BUILD),
        ("manual_image", "MANUAL", ImageType.MANUAL),
        ("image_from_docker", "MANUAL", ImageType.MANUAL),
        ("image_from_dict", "PULL", ImageType.PULL),
    ],
)
def test_exists(request, image_fixture, expected_action, expected_type):
    image = request.getfixturevalue(image_fixture)
    result = image.exists()
    assert isinstance(result, bool)
    if str(image.action) in ["PULL", "BUILD"]:
        assert result is True
        assert image.docker_image is not None
        
@pytest.mark.parametrize(
    "image_fixture,expected_action,expected_type",
    [
        ("pull_image", "PULL", ImageType.PULL),
        ("build_image", "BUILD", ImageType.BUILD),
        ("manual_image", "MANUAL", ImageType.MANUAL),
        ("image_from_docker", "MANUAL", ImageType.MANUAL),
        ("image_from_dict", "PULL", ImageType.PULL),
    ],
)
def test_load_sets_attributes(request, image_fixture, expected_action, expected_type):
    image = request.getfixturevalue(image_fixture)
    image.load()
    assert hasattr(image, "id")
    assert hasattr(image, "labels")
    assert hasattr(image, "tags")
    assert isinstance(image.meta, ImageMeta)
    for key in image.meta.dict:
        assert hasattr(image, key)
        
@pytest.mark.parametrize(
    "image_fixture,expected_action,expected_type",
    [
        ("pull_image", "PULL", ImageType.PULL),
        ("build_image", "BUILD", ImageType.BUILD),
        ("manual_image", "MANUAL", ImageType.MANUAL),
        ("image_from_docker", "MANUAL", ImageType.MANUAL),
        ("image_from_dict", "PULL", ImageType.PULL),
    ],
)
def test_setup_behavior(request, image_fixture, expected_action, expected_type):
    image = request.getfixturevalue(image_fixture)
    if expected_action == "MANUAL":
        image.setup()
    if str(image.action) in ["PULL", "BUILD"]:
        assert image.exists()
    else:
        assert True
        
@pytest.mark.parametrize(
    "image_fixture,expected_action,expected_type",
    [
        ("pull_image", "PULL", ImageType.PULL),
        ("build_image", "BUILD", ImageType.BUILD),
        ("manual_image", "MANUAL", ImageType.MANUAL),
        ("image_from_docker", "MANUAL", ImageType.MANUAL),
        ("image_from_dict", "PULL", ImageType.PULL),
    ],
)
def test_image_properties(image_fixture, expected_action, expected_type, request):
    image = request.getfixturevalue(image_fixture)
    assert str(image.action) == expected_action
    assert image.type == expected_type
    assert isinstance(image.status, str)
    assert image.full_status.startswith("[")
    assert isinstance(image.dict, dict)
    assert image.name == f"{image.repository}:{image.tag}"
    
