import re
from pathlib import Path

DROP = re.compile(r"#!.*\n")
EXPAND = re.compile(r'expand\("(.*)" *, *([^\)]*)\) *{([\s\S]*?)}')
TEMPLATE = re.compile(r"template *\( *\) * {[\S\s]*?}")
MACRO = re.compile(r" *macro *\(([^,]*),.*?(\$[^\)]*\)) *")


def convert(target, verbose=False):
    text = target.read_text()
    text_out = text

    # find and process any expand() blocks
    for match in EXPAND.finditer(text):
        if verbose:
            print(f"Found expand block named '{match.group(2)}'")
            print(f"  macros: {match.group(3)}")

        substitutes = macro2substitute(match.group(3))
        include_path = Path(match.group(1))
        include_path = include_path.with_suffix(".template")
        include = f'include "{include_path}"'

        all = "\n".join([substitutes, include])

        text_out = EXPAND.sub(all, text_out, 1)

    # now remove redundant VDCT directives
    text_out = DROP.sub("", text_out)
    text_out = TEMPLATE.sub("", text_out)

    new_file = target.with_suffix(".template")
    with new_file.open("w") as out_f:
        out_f.write(text_out)


def macro2substitute(text):
    text_out = ""
    for match in MACRO.finditer(text):
        text_out += f'substitute "{match.group(1)}={match.group(2)}"\n'
    return text_out
