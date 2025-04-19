"""Module entry point."""

from wordly.cli import main
import asyncio


def run():
    asyncio.run(main())


if __name__ == "__main__":
    run()
