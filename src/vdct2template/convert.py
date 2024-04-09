from pathlib import Path

from .expansion import Expansion
from .regex import DROP


def convert(folder: Path, builder_txt: str):
    """
    function to oversee conversion of a set of VDB files to template files.
    """
    targets = list(folder.glob("*.vdb"))

    for target in targets:
        expansion = Expansion(target, folder)
        if expansion.parse_expands() > 0:
            print(f"writing expansion {expansion.template_path}")
            expansion.template_path.write_text(expansion.text)

            for file, text in expansion.process_includes():
                print(f"writing template {file}")
                file.write_text(text)

    # process the remaining (flat) vdbs
    all_vdb_files = {target.name for target in targets}
    unprocessed = all_vdb_files - set(Expansion.processed)

    for file in unprocessed:
        path = folder / file
        template_path = path.with_suffix(".template")

        text = path.read_text()
        text = DROP.sub("", text)

        print(f"writing flat {file}")
        template_path.write_text(text)

    # give warnings if there are inconsistent macro substitutions
    Expansion.validate_includes()
