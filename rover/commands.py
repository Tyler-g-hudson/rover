import os
import pathlib
import subprocess
from typing import Dict, Iterable, Union

import pooch

from ._utils import check_registry_files, delete_registry_files, kvp_parse


def fetch(
        repo: Union[os.PathLike[str], str],
        url: str,
        files: Iterable[str],
        no_cache: bool = False
) -> None:
    """
    Acquire a copy of a repository.

    Parameters
    ----------
    repo : os.PathLike[str]
        The name of the repository.
    url : str
        The URL of the online file repo.
    files : Iterable[str]
        A set of files and hashes in "[FILE]=[HASH]" format.
    no_cache : bool, optional
        If true, delete and redownload all requested files. Defaults to False.
    """
    print(f"Rover is retrieving samples from {repo}!")
    # The registry is the set of files and hashes in dictionary format.
    registry: Dict[str, str] = kvp_parse(kvp_strings=files)

    mnt_dir = os.environ["MOUNT_LOCATION"]
    # The "base path" is the absolute location of the mount directory.
    base_path: str = str(pathlib.Path(mnt_dir).absolute()) + "/"
    # The repository path is the base path with "/[REPO_NAME]" appended to it.
    repo_path: str = f"{base_path}{repo}"
    # A .gitignore file either exists at the base path or will be put there.
    gitignore: str = f"{base_path}.gitignore"

    if no_cache:
        # for item in repo, if item exists, remove it.
        delete_registry_files(registry=registry, repo_path=repo_path)
    else:
        # for item in repo, hash local version. if hash != repo hash, error.
        check_registry_files(registry=registry, repo_path=repo_path)

    # Build the repository directory if it doesn't already exist.
    if not pathlib.Path(base_path).is_dir():
        subprocess.run(["mkdir", "-p", base_path])
    if not pathlib.Path(repo_path).is_dir():
        subprocess.run(["mkdir", "-p", repo_path])
    if not pathlib.Path(gitignore).is_file():
        with open(gitignore, "w") as f:
            f.write("*\n")

    # Set up the Pooch repository object.
    poppy: pooch.Pooch = pooch.create(
        path=repo_path,
        base_url=url,
        registry=registry,
        allow_updates=True
    )

    # Fetch all of the requested files.
    for key in registry:
        poppy.fetch(fname=key, progressbar=True)
    print(f"Rover has returned all samples in {repo}!")
