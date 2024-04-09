from pathlib import Path
from tempfile import TemporaryDirectory
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
        help="Print the version and exit",
    ),
    targets: List[Path] = typer.Argument(
        ...,
        help="list of vdb files to convert to template files.",
        exists=True,
        dir_okay=False,
        resolve_path=True,
    ),
    use_builder: bool = typer.Option(
        True,
        help="Use the builder.py file to look for direct references to template files.",
    ),
    verbose: bool = typer.Option(
        False, "--verbose", "-v", help="Print more information."
    ),
    builder: Optional[Path] = typer.Option(
        None,
        help="Path to the builder file.",
        exists=True,
        dir_okay=False,
        resolve_path=True,
    ),
):
    """
    VDCT to template conversion function.

    Converts all passed VDCT files to template files. Recommended invocation
    is to pass all VDCT files for a support module in a single call using
    a glob pattern.

    This function assumes that all referenced VDCT files in the expand() blocks
    will be in the same folder.

    We can use the builder.py file to check for direct references to template files
    Use --no-use-builder to disable this feature. Direct references to a template
    file is an error because we need to modify all macro names to add a _ prefix
    in templated files.

    This tool converts VDCT files to template files. It looks for expand() blocks
    in the VDCT files. If these are found then it will also convert all of the
    referenced files to template files. In referenced files the macro names will
    all have _ prefix added because MSI does not support substituting a macro with
    it's own name and passing a default. This is a workaround to that limitation.

    The original expands() block is replaced with a series of substitute
    and include MSI directives.

    The resulting set of templates can be expanded natively by MSI without the
    need for VDCT. The resulting DB files should be equivalent to the original.
    """

    builder = builder or Path(targets[0].parent.parent.parent / "etc" / "builder.py")
    builder_txt = builder.read_text()

    tmp_dir = Path(TemporaryDirectory().name)

    for target in targets:
        convert(target=target, tmp_dir=tmp_dir, builder_txt=builder_txt)


# test with:
#     pipenv run python -m ibek
if __name__ == "__main__":
    typer.run(main)
