from x17_container.dockers.image.image import Image
from x17_container.dockers.image.imagebuild import ImageBuild
import pytest
import tempfile

def test_build_init_from_direct_args():
    param = ImageBuild(
        path="/tmp/x17",
        dockerfile="Dockerfile",
        buildargs={"KEY": "value"},
        squash=True,
        labels={"maintainer": "x17"}
    )
    assert param.path == "/tmp/x17"
    assert param.dockerfile == "Dockerfile"
    assert param.buildargs == {"KEY": "value"}
    assert param.labels == {"maintainer": "x17"}
    assert param.dict["squash"] is True
    assert param.is_valid() is True
    assert isinstance(param.export(), dict)

def test_build_init_from_params_dict():
    params = {
        "path": "/tmp/from-dict",
        "dockerfile": "Dockerfile.build",
        "buildargs": {"MODE": "debug"},
        "rm": False,
        "extra_hosts": {"test": "127.0.0.1"},
    }
    param = ImageBuild(params=params)
    assert param.path == "/tmp/from-dict"
    assert param.dockerfile == "Dockerfile.build"
    assert param.buildargs == {"MODE": "debug"}
    assert param.rm is False
    assert param.extra_hosts == {"test": "127.0.0.1"}
    assert param.is_valid() is True

def test_build_invalid_when_no_path_or_fileobj():
    param = ImageBuild()
    assert param.is_valid() is False
    assert isinstance(param.dict, dict)

def test_build_repr_and_str():
    param = ImageBuild(path="/path/to/context", dockerfile="Dockerfile")
    assert str(param) == "/path/to/context"
    assert "ImageBuild" in repr(param)
    assert "path=" in repr(param)
    

def test_build_with_temp_directory():
    with tempfile.TemporaryDirectory() as tmpdir:
        param = ImageBuild(path=tmpdir)
        assert param.path == tmpdir
        assert param.is_valid() is True

def test_imagebuild_from_dict():
    build_dict = {
        "path": "/tmp/project",
        "dockerfile": "Dockerfile",
        "tag": "myimage:1.0",
        "buildargs": {"KEY": "value"},
        "labels": {"maintainer": "x"},
        "platform": "linux/arm64",
    }

    build = ImageBuild.from_dict(build_dict)

    assert build.path == "/tmp/project"
    assert build.dockerfile == "Dockerfile"
    assert build.tag == "myimage:1.0"
    assert build.buildargs == {"KEY": "value"}
    assert build.labels == {"maintainer": "x"}
    assert build.platform == "linux/arm64"
    assert build.is_valid() is True

    exported = build.export()
    for key in build_dict:
        assert key in exported

    assert "ImageBuild(" in repr(build)
    assert str(build) == "/tmp/project"
    
    