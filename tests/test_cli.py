import subprocess
import sys

from vdct2template import __version__


def test_cli_version():
    cmd = [sys.executable, "-m", "vdct2template", "--version"]
    assert subprocess.check_output(cmd).decode().strip() == __version__
