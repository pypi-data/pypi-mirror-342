from bluer_options import string

from bluer_objects import file, objects
from bluer_objects import storage


def test_storage():
    object_name = objects.unique_object("test_storage")

    depth = 10

    for filename in [
        "this.yaml",
        "that.yaml",
        "subfolder/this.yaml",
        "subfolder/that.yaml",
    ]:
        assert file.save_yaml(
            objects.path_of(
                object_name=object_name,
                filename=filename,
            ),
            {
                string.random(length=depth): string.random(length=depth)
                for _ in range(depth)
            },
        )

    for filename in [
        "this.yaml",
        "subfolder/this.yaml",
    ]:
        assert storage.upload(
            object_name=object_name,
            filename=filename,
        )

    assert storage.upload(object_name=object_name)

    for filename in [
        "this.yaml",
        "subfolder/this.yaml",
    ]:
        assert storage.download(
            object_name=object_name,
            filename=filename,
        )

    assert storage.download(object_name=object_name)
