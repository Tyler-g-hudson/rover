import argparse
import sys
from typing import Sequence

from .commands import fetch


def setup_parser() -> argparse.ArgumentParser:
    """
    Create a top-level argument parser.

    Returns
    -------
    argparse.ArgumentParser
        The parser.
    """

    def help_formatter(prog): return argparse.HelpFormatter(
        prog,
        max_help_position=60
    )

    parser = argparse.ArgumentParser(
        prog=__package__,
        formatter_class=help_formatter
    )

    # Add arguments
    subparsers = parser.add_subparsers(dest="command")

    fetch_parser = subparsers.add_parser("fetch", help="Fetch a group of files.",
                                         formatter_class=help_formatter)
    fetch_parser.add_argument(
        "--repo", "-r", type=str,
        help='The name of the repository being fetched.'
    )
    fetch_parser.add_argument(
        "--url", "-u", type=str,
        help='The URL of the repository.'
    )
    fetch_parser.add_argument(
        "--file", "-f", metavar="FILENAME=HASH", nargs="+", dest="files",
        help="A file and its checksum hash, separated by '='."
    )
    fetch_parser.add_argument(
        "--no-cache", action="store_true", default=False,
        help="If used, delete and redownload all files."
    )

    return parser


def main(
    args: Sequence[str] = sys.argv[1:]
):
    parser = setup_parser()
    args_parsed = parser.parse_args(args)
    command: str = args_parsed.command
    if command is None:
        insufficient_subcommands_message(
            subcommand="The rover program",
            command_str="rover"
        )
    command = command.lower()
    del args_parsed.command
    if command == "fetch":
        fetch(**vars(args_parsed))


def insufficient_subcommands_message(
    subcommand: str,
    command_str: str
) -> None:
    """
    Print an error string when an incomplete set of commands is given.

    Parameters
    ----------
    subcommand : str
        The subcommand name.
    command_str : str
        The full command string up to the subcommand (e.g. "rover fetch")
    """
    print(f"\n  {subcommand} requires further subcommands!")
    print(f"  For more info: \"{command_str} -h\"\n")
    exit(1)
