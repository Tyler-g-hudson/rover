import os
import pathlib
import subprocess
from typing import Dict, Iterable, Union

import pooch

from ._utils import kvp_parse


def fetch(
        repo: Union[os.PathLike[str], str],
        url: str,
        files: Iterable[str]
):
    registry: Dict[str, str] = kvp_parse(kvp_strings=files)

    mnt_dir = "./mnt/"
    base_path: str = str(pathlib.Path(f"{mnt_dir}Rover/").absolute()) + "/"
    path: str = f"{base_path}{repo}"
    gitignore: str = f"{mnt_dir}/.gitignore"

    # Build the repository directory if it doesn't already exist.
    if not pathlib.Path(path).is_dir():
        subprocess.run(["mkdir", "-p", path])
    if not pathlib.Path(gitignore).is_file():
        with open(gitignore, "w") as f:
            f.write("*\n")

    # Set up the Pooch repository object.
    poppy: pooch.Pooch = pooch.create(
        path=path,
        base_url=url,
        registry=registry,
        allow_updates=True
    )

    # Fetch all of the requested files.
    for key in registry:
        poppy.fetch(
            fname=key
        )
