import os

from blueness import module

from bluer_objects import NAME as MY_NAME
from bluer_objects import file
from bluer_objects.README.functions import build
from bluer_objects.README.items import Items
from bluer_objects.logger import logger

MY_NAME = module.name(__file__, MY_NAME)


def build_me() -> bool:
    from bluer_objects import NAME, VERSION, REPO_NAME, ICON

    return all(
        build(
            path=os.path.join(file.path(__file__), readme["path"]),
            ICON=ICON,
            NAME=NAME,
            VERSION=VERSION,
            REPO_NAME=REPO_NAME,
        )
        for readme in [
            {"path": "../.."},
            {"path": "."},
        ]
    )
