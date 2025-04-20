import os
from typing import List
import glob
from tqdm import tqdm

from blueness import module
from bluer_objects import objects, file
from bluer_objects.env import abcli_path_git

from bluer_sandbox import NAME
from bluer_sandbox.logger import logger


NAME = module.name(__file__, NAME)


def publish(
    object_name: str,
    list_of_extensions: List[str],
    prefix: str = "",
    log: bool = True,
) -> bool:
    logger.info(
        "{}.publish: {}/{}.* for {}".format(
            NAME,
            object_name,
            prefix,
            ", ".join(list_of_extensions),
        )
    )

    for extension in tqdm(list_of_extensions):
        for filename in glob.glob(
            objects.path_of(
                filename=f"{prefix}*.{extension}",
                object_name=object_name,
            )
        ):
            published_filename = os.path.join(
                abcli_path_git,
                "assets",
                object_name,
                file.name_and_extension(filename),
            )

            if extension in ["png", "jpg", "jpeg", "gif", "txt"]:
                if not file.copy(
                    filename,
                    published_filename,
                    log=log,
                ):
                    return False

    logger.info(f"🔗  https://github.com/kamangir/assets/tree/main/{object_name}")

    return True
