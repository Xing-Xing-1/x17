import pytest
from copy import deepcopy
from x17_container.dockers.image.imagemeta import ImageMeta


def sample_dict():
    return {
        "repotags": ["myrepo:latest"],
        "repodigests": ["sha256:abc123"],
        "parent": "parentid",
        "comment": "This is a test image",
        "created": "2023-01-01T00:00:00Z",
        "docker_version": "20.10.7",
        "author": "Xing",
        "config": {"Env": ["PATH=/usr/bin"]},
        "architecture": "amd64",
        "variant": "v1",
        "os": "linux",
        "size": 123456,
        "graph_driver": {"Name": "overlay2"},
        "rootfs": {"type": "layers", "layers": ["abc", "def"]},
        "metadata": {"lastTagTime": "2023-01-01T00:00:00Z"},
        "descriptor": {"mediaType": "application/vnd.docker.container.image.v1+json"}
    }


def test_init_with_params():
    meta = ImageMeta(params=deepcopy(sample_dict()))
    assert meta.repotags == ["myrepo:latest"]
    assert meta.architecture == "amd64"
    assert meta.is_valid()
    assert "ImageMeta(" in repr(meta)


def test_init_with_explicit_arguments():
    d = sample_dict()
    meta = ImageMeta(
        repotags=d["repotags"],
        repodigests=d["repodigests"],
        parent=d["parent"],
        comment=d["comment"],
        created=d["created"],
        docker_version=d["docker_version"],
        author=d["author"],
        config=d["config"],
        architecture=d["architecture"],
        variant=d["variant"],
        os=d["os"],
        size=d["size"],
        graph_driver=d["graph_driver"],
        rootfs=d["rootfs"],
        metadata=d["metadata"],
        descriptor=d["descriptor"],
    )
    assert meta.dict == d
    assert meta.is_valid()

def test_empty_image_meta():
    meta = ImageMeta()
    expected = {
        "repotags": [],
        "repodigests": [],
        "parent": None,
        "comment": None,
        "created": None,
        "docker_version": None,
        "author": None,
        "architecture": None,
        "variant": None,
        "os": None,
        "config": {},
        "size": 0,
        "graph_driver": {},
        "rootfs": {},
        "metadata": {},
        "descriptor": {},
    }
    assert meta.dict == expected
    assert not meta.is_valid()


def test_export_matches_dict():
    meta = ImageMeta(params=sample_dict())
    assert meta.export() == meta.dict
    
def test_image_meta_from_dict():
    sample_dict = {
        "repotags": ["myimage:latest"],
        "repodigests": ["sha256:abc123"],
        "parent": "parent_id",
        "comment": "some comment",
        "created": "2025-06-20T00:00:00Z",
        "docker_version": "20.10.5",
        "author": "x",
        "config": {"Env": ["PATH=/usr/local/bin"]},
        "architecture": "amd64",
        "variant": "v7",
        "os": "linux",
        "size": 123456,
        "graph_driver": {"Name": "overlay2"},
        "rootfs": {"type": "layers"},
        "metadata": {"lastTagTime": "2025-06-20T01:00:00Z"},
        "descriptor": {"digest": "sha256:abc123"},
    }

    meta = ImageMeta.from_dict(sample_dict)
    assert meta.repotags == ["myimage:latest"]
    assert meta.created == "2025-06-20T00:00:00Z"
    assert meta.size == 123456
    assert meta.is_valid()
    assert isinstance(meta.dict, dict)
    assert meta.export() == meta.dict
    assert "ImageMeta(" in repr(meta)
    assert str(meta) == "myimage:latest"
    