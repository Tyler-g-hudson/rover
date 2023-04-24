from typing import Dict, Iterable


def kvp_parse (
        kvp_strings: Iterable[str]
) -> Dict[str, str]:
    """
    Splits a set of strings into key-value pairs in a dictionary.

    Parameters
    ----------
    kvp_strings : Iterable[str]
        _description_

    Returns
    -------
    Dict[str, str]
        _description_

    Raises
    ------
    ValueError
        _description_
    """
    ret_dict = {}
    for value in kvp_strings:
        kvp = value.split(":")
        if len(kvp) != 2:
            raise ValueError(f"{value} is not a key-value pair.")
        key = kvp[0]
        ret_dict[key] = kvp[1]
    return ret_dict
