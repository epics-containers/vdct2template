import re

# all redundant VDB header/footer info starts with #!
DROP = re.compile(r"#!.*\n")
