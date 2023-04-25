import os
import pathlib
import subprocess
from textwrap import dedent
from typing import Dict, Iterable, Union

import pooch

from ._exceptions import HashCollisionError


def kvp_parse(
        kvp_strings: Iterable[str]
) -> Dict[str, str]:
    """
    Splits a set of strings into key-value pairs in a dictionary.

    Parameters
    ----------
    kvp_strings : Iterable[str]
        The set of strings to be parsed. Should be in "[KEY]:[VALUE]" format.

    Returns
    -------
    Dict[str, str]
        A dictionary containing the key-value pairs.

    Raises
    ------
    ValueError
        If a given string is improperly formatted.
    """
    ret_dict = {}
    # Populate the above dictionary with each of the strings.
    for value in kvp_strings:
        kvp = value.split(":")
        # If the length of the split string is not 2, then too few or many ":"
        # characters were used. Reject this string.
        if len(kvp) != 2:
            raise ValueError(f"{value} is not a key-value pair.")
        # Otherwise, the key is the first split string and the value is the second one.
        key = kvp[0]
        ret_dict[key] = kvp[1]
    return ret_dict


def delete_registry_files(
        registry: Iterable[str],
        repo_path: Union[os.PathLike[str], str]
) -> None:
    """
    Deletes all of the local copies of files in a registry, if they exist.

    Parameters
    ----------
    registry : Iterable[str]
        The registry of files, in iterable format.
    repo_path : os.PathLike[str]
        The path to the repository where the registry files might exist.
    """
    # If the repository doesn't already exist, there is nothing to remove.
    if not pathlib.Path(repo_path).is_dir():
        return
    # Otherwise, delete every file in the registry that exists in the repostiory.
    for file in registry:
        filepath = f"{repo_path}/{file}"
        if pathlib.Path(filepath).is_file():
            subprocess.run(["rm", "filepath"])


def check_registry_files(
        registry: Dict[str, str],
        repo_path: Union[os.PathLike[str], str]
) -> None:
    """
    Checks the hashes of all files in a registry vs. given hashes.

    Parameters
    ----------
    registry : Dict[str, str]
        The registry of files, in dictionary format.
    repo_path : os.PathLike[str]
        The path to the repository where the registry files might exist.
    """
    # If the repository doesn't already exist, there is nothing to check.
    if not pathlib.Path(repo_path).is_dir():
        return
    # Otherwise, check every file in the registry that exists in the repostiory.
    for file in registry:
        known_hash = registry[file]
        filepath = f"{repo_path}/{file}"
        # If the local file doesn't exist, move on.
        if not pathlib.Path(filepath).is_file():
            continue
        # Hash the local file and compare that hash to the input hash.
        repo_hash = pooch.file_hash(filepath)
        if not repo_hash == known_hash:
            # If the hashes are different, this constitutes an error.
            # Either the user's local file has changed or their hash was modified.
            # In either case, throw an error.
            raise HashCollisionError(
                message=dedent(f"""
                {file} local hash differs from known-good hash!
                This means that your local file differs from the known file.
                Please check your file and, if you would like to proceed,
                use --no-cache.
                """).strip()
            )
