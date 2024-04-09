import re
from pathlib import Path
from typing import List

from vdct2template.macros import Macros

EXPAND = re.compile(r'expand\("(.*)" *, *([^\)]*)\) *{([\s\S]*?)}')


class Expansion:
    """
    A class to represent a VDB file that contains expands() blocks.

    Provides the necessary conversion to MSI include/substitute statements.
    """

    # class level list of all Expansion instances created
    Expansions: List["Expansion"] = []

    def __init__(self, filename) -> None:
        """
        Constructor: set up properties
        """
        self.vdb_filename = filename
        self.template_filename = filename.with_suffix(".template")
        self.includes = []
        self.text = filename.read_text()

        Expansion.Expansions.append(self)

    def parse_expands(self) -> int:
        """
        Parse the expands() blocks in the VDB file.

        Updates the class attribute substitutions with the macro substitutions parsed.
        Updates the class attribute text with the VDB file text with the expands()
        blocks processed into MSI substitute/include statements.

        returns the number of expands() blocks found.
        """

        expands = EXPAND.findall(self.text)
        if not expands:
            return 0

        for match in expands:
            # match: 0=include path, 1=name, 2=macro text
            include_path = Path(match[0])
            macros = Macros(include_path, match[2])
            self.includes.append((include_path, macros))

            # replace the expands() block with the MSI directives
            self.text = EXPAND.sub(macros.render_include(), self.text, 1)

        return len(expands)
