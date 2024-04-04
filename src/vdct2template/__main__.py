from pathlib import Path
from typing import List, Optional

import typer

from . import __version__
from .convert import convert

__all__ = ["main"]


cli = typer.Typer()


def version_callback(value: bool):
    if value:
        typer.echo(__version__)
        raise typer.Exit()


@cli.command()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Print the version of ibek and exit",
    ),
    targets: List[Path] = typer.Argument(
        ...,
        help="list of vdb files to convert to template files.",
        exists=True,
        dir_okay=False,
        resolve_path=True,
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Print more information."
    ),
):
    """
    VDCT to template convertor.
    """

    for target in targets:
        typer.echo(f"Converting {target} to template file.")
        convert(target=target, verbose=verbose)


# test with:
#     pipenv run python -m ibek
if __name__ == "__main__":
    typer.run(main)
