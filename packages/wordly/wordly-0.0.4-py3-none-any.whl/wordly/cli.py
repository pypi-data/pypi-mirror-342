"""Command line options."""

import argparse
import asyncio
from collections.abc import Sequence
from wordly import __app_name__, __app_description__, __version__, __epilog__
from wordly.words import Word


async def print_definition(word: str, hostname: str, port: int):
    w = Word(word, hostname=hostname, port=port)
    definition = await w.adefinition
    print(definition)


async def main(argv: Sequence[str] | None = None):
    parser = argparse.ArgumentParser(
        prog=__app_name__,
        description=__app_description__,
        epilog=__epilog__,
    )
    opt = parser.add_argument

    opt("words", nargs="+", help="One or more words to define.")
    opt("-v", "--version", version=__version__, action="version")
    opt(
        "-p",
        "--port",
        type=int,
        default=2628,
        help="Specify the port number. Default: 2628",
    )
    opt(
        "-H",
        "--hostname",
        type=str,
        default="dict.org",
        help="Specify the server. Default: dict.org",
    )

    args = vars(parser.parse_args(argv))

    tasks = [
        print_definition(word, args["hostname"], args["port"]) for word in args["words"]
    ]

    await asyncio.gather(*tasks)
