from pathlib import Path
from typing import List

from .expansion import Expansion


def convert(targets: List[Path], builder_txt: str):
    """
    function to oversee conversion of a set of VDB files to template files.
    """
    for target in targets:
        expansion = Expansion(target)
        if expansion.parse_expands() > 0:
            print(f"writing expansion {expansion.template_path}")
            expansion.template_path.write_text(expansion.text)

            for file, text in expansion.process_includes():
                print(f"writing template {file}")
                file.write_text(text)

    Expansion.validate_includes()

    # find and process any expand() blocks
    # expands = EXPAND.findall(text)
    # if expands:
    #     for match in expands:
    #         include_path = Path(match[0])
    #         substitutes = _macro2substitute(
    #             match[2], include_path, target.parent, builder_txt
    #         )
    #         include = f'include "{include_path.with_suffix(".template")}"'
    #         all = "\n".join([substitutes, include])

    #         text_out = EXPAND.sub(all, text_out, 1)

    # templates = TEMPLATE.findall(text)
    # # expanded template files are handled by macro2substitute
    # if not templates:
    #     print(f"writing expansion conversion for {target}")
    #     text_out = _drop_vdct(text_out)
    #     target.with_suffix(".template").write_text(text_out)
