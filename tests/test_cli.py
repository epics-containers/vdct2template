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

    cmd = [
        "--no-use-builder",
        *list(map(str, data.glob("*.vdb"))),
    ]
    runner.invoke(cli, cmd)
