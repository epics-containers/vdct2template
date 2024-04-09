import subprocess
import sys
from pathlib import Path

from typer.testing import CliRunner

from vdct2template import __version__
from vdct2template.__main__ import cli

runner = CliRunner()


def test_cli_version():
    cmd = [sys.executable, "-m", "vdct2template", "--version"]
    assert subprocess.check_output(cmd).decode().strip() == __version__


def test_convert():
    data = (Path(__file__).parent / "data").resolve()

    templates = data.glob("*.template")
    for template in templates:
        template.unlink()

    cmd = [
        "--no-use-builder",
        *list(map(str, data.glob("*.vdb"))),
    ]
    runner.invoke(cli, cmd)

    # verify all vdb got a template conversion and that the template looks right
    results = (Path(__file__).parent / "results").resolve()
    for vdb in data.glob("*.vdb"):
        assert (vdb.with_suffix(".template")).exists(), f"{vdb.name} not converted"
        assert (vdb.with_suffix(".template")).read_text() == (
            results / vdb.name
        ).read_text(), f"{vdb.name} not conversion does not match expected result"
