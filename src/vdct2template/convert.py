import re
from pathlib import Path

from .expansion import Expansion

# all redundant VDB header info starts with #!
DROP = re.compile(r"#!.*\n")
# template blocks are also redundant
TEMPLATE = re.compile(r"template *\( *\) * {[\S\s]*?}")


def convert(target: Path, tmp_dir: Path, builder_txt: str):
    expansion = Expansion(target)
    if expansion.parse_expands() > 0:
        expansion.template_filename.write_text(expansion.text)

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


def tidy_up(root_folder: Path):
    # mop up the files that have no expand() and not referenced from an expand()
    for vdb in root_folder.glob("*.vdb"):
        pass


def _drop_vdct(text: str) -> str:
    # remove redundant VDCT directives
    text = DROP.sub("", text)
    text = TEMPLATE.sub("", text)

    return text


# def _macro2substitute(
#     macro_text: str,
#     include_path: Path,
#     folder: Path,
#     builder_txt: str,
# ):
#     substitutes_out = ""
#     vdb_file = folder / include_path
#     template_file = vdb_file.with_suffix(".template")
#     vdb_text = vdb_file.read_text()

#     for match in MACRO.finditer(macro_text):
#         # add underscore to template macro otherwise defaults don't get pushed down
#         substitutes_out += f'substitute "_{match.group(1)}={match.group(2)}"\n'
#         vdb_text = vdb_text.replace(f"$({match.group(1)})", f"$(_{match.group(1)})")

#     if str(template_file.name) in builder_txt:
#         print(
#             f"WARNING: templated {template_file} is directly "
#             "referenced in builder.py"
#         )

#     vdb_text = _drop_vdct(vdb_text)

#     print(f"writing template {template_file}")
#     template_file.write_text(vdb_text)

#     return substitutes_out
