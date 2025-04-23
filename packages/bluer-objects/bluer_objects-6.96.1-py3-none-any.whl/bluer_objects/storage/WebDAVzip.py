import glob
import os
from typing import Tuple, List
from webdav3.client import Client

from bluer_objects.storage.base import StorageInterface
from bluer_objects import env, file, path
from bluer_objects import objects
from bluer_objects.host import zip, unzip
from bluer_objects.logger import logger


# tars the objects to avoid 'content-length' - see WebDAVInterface.
class WebDAVzipInterface(StorageInterface):
    name = "webdavzip"

    def __init__(self):
        super().__init__()

        config = {
            "webdav_hostname": env.WEBDAV_HOSTNAME,
            "webdav_login": env.WEBDAV_LOGIN,
            "webdav_password": env.WEBDAV_PASSWORD,
        }

        self.client = Client(config)

    def download(
        self,
        object_name: str,
        filename: str = "",
        log: bool = True,
    ) -> bool:
        object_path = objects.object_path(object_name=object_name)
        zip_filename = f"{object_path}.zip"

        try:
            if not self.client.check(remote_path=f"{object_name}.zip"):
                logger.warning(f"{object_name} doesn't exist.")
                return True
        except Exception as e:
            logger.error(e)
            return False

        try:
            self.client.download_sync(
                remote_path=f"{object_name}.zip",
                local_path=zip_filename,
            )
        except Exception as e:
            logger.error(e)
            return False

        if not unzip(
            zip_filename=zip_filename,
            output_folder=object_path,
            log=log,
        ):
            return False

        return super().download(
            object_name=object_name,
            log=log,
        )

    def ls(
        self,
        object_name: str,
        where: str = "local",
    ) -> Tuple[bool, List[str]]:
        if where == "local":
            object_path = objects.object_path(
                object_name=object_name,
            )

            return True, [
                os.path.relpath(filename, start=object_path)
                for filename in glob.glob(
                    os.path.join(
                        object_path,
                        "**",
                        "*",
                    ),
                    recursive=True,
                )
                if os.path.isfile(filename)
            ]

        if where == "cloud":
            try:
                if self.client.check(remote_path=f"{object_name}.zip"):
                    return True, [f"{object_name}.zip"]
            except Exception as e:
                logger.error(e)
                return False, []

            return True, []

        logger.error(f"Unknown 'where': {where}")
        return False, []

    def upload(
        self,
        object_name: str,
        filename: str = "",
        log: bool = True,
    ) -> bool:
        object_path = objects.object_path(object_name=object_name)

        if not zip(
            zip_filename=f"../{object_name}.zip",
            input_folder=".",
            work_dir=object_path,
            log=log,
        ):
            return False

        zip_filename = f"{object_path}.zip"
        try:
            self.client.upload_sync(
                remote_path=f"{object_name}.zip",
                local_path=zip_filename,
            )
        except Exception as e:
            logger.error(e)
            return False

        return super().upload(
            object_name=object_name,
            log=log,
        )
