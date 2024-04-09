from pathlib import Path

from .expansion import Expansion


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

    Expansion.validate_includes()

    # make a set of all names of all vdb files
    all_vdb_files = {target.name for target in targets}

    unprocessed = all_vdb_files - set(Expansion.processed)
    for file in unprocessed:
        pass
