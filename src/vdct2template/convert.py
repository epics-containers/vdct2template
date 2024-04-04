import re
from pathlib import Path

DROP = re.compile(r"#!.*\n")
EXPAND = re.compile(r'expand\("(.*)" *, *([^\)]*)\) *{([\s\S]*?)}')
TEMPLATE = re.compile(r"template *\( *\) * {[\S\s]*?}")
MACRO = re.compile(r" *macro *\(([^,]*),.*?(\$[^\)]*\)) *")


def convert(target: Path):
    text_out = text = target.read_text()

    # find and process any expand() blocks
    expands = EXPAND.findall(text)
    if expands:
        for match in expands:
            include_path = Path(match[0])
            include_path = include_path.with_suffix(".template")
            substitutes = macro2substitute(match[2], include_path, target.parent)
            include = f'include "{include_path}"'
            all = "\n".join([substitutes, include])

            text_out = EXPAND.sub(all, text_out, 1)

    templates = TEMPLATE.findall(text)
    # expanded template files are handled by macro2substitute
    if not templates:
        write_template_file(target, text_out)


def write_template_file(target: Path, text_out: str):
    # remove redundant VDCT directives
    text_out = DROP.sub("", text_out)
    text_out, n = TEMPLATE.subn("", text_out)

    new_file = target.with_suffix(".template")
    with new_file.open("w") as out_f:
        out_f.write(text_out)


def macro2substitute(macro_text: str, include_path: Path, folder: Path):
    substitutes_out = ""
    vdb_file = folder / include_path
    vdb_text = vdb_file.read_text()

    for match in MACRO.finditer(macro_text):
        # add underscore to template macro otherwise defaults don't get pushed down
        substitutes_out += f'substitute "_{match.group(1)}={match.group(2)}"\n'
        vdb_text = vdb_text.replace(f"$({match.group(1)})", f"$(_{match.group(1)})")

    write_template_file(vdb_file.with_suffix(".template"), vdb_text)
    return substitutes_out
