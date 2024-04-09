import re
from pathlib import Path
from typing import Dict

MACRO = re.compile(r' *macro *\(([^,]*), *"([^"]*) *')


class Macros:
    """
    A class to represent the set of macro substitutions in an expands() block.
    """

    def __init__(self, filename: Path, macros_text: str) -> None:
        """
        Parse the macros section of an expands() block.

        Populate the class attribute macros with the macro substitutions found.
        """
        self.vdb_filename = filename
        self.include_filename = filename.with_suffix(".template")
        self.macros: Dict[str, str] = {}

        for match in MACRO.finditer(macros_text):
            self.macros[match.group(1)] = match.group(2)

    def render_include(self):
        """
        Convert the macro name, values in this class into MSI substitutes
        directives followed by an include directive.

        IMPORTANT: All subordinate template macro names have a _ suffix added

        This means that, for example:
            macro(ilk0, "$(ilk0=unused)

        becomes:
            substitute "_ilk0=$(ilk0=unused)"

        If we did not change the macro name then MSI would not use the default
        value because it sees 'ilk0' as already defined.

        NOTE: this means that when rendering the subordinate templates we need
        to make the same macro name changes.
        """
        include = ""
        for name, value in self.macros.items():
            include += f'substitute "_{name}={value}"\n'

        include += f'\ninclude "{self.include_filename}"\n'

        return include
