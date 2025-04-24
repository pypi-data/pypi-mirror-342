import click

from segmock.app import Segmock
from segmock.version import SEGMOCK_VERSION


@click.command()
@click.version_option(SEGMOCK_VERSION)
def main() -> None:
    Segmock().run()


if __name__ == "__main__":
    main()
