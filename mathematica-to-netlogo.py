import sys
import re

f = open(sys.argv[1], 'r')

for line in f:
  if len(line) > 4: # only let in valid lines

    # get rid of garbage chars at line boundaries
    line = line.lstrip('\r\n\l {').rstrip('\r\n\l ,}')

    # NL var setting syntax
    r = re.compile(r'^([A-Za-z0-9_]+) -> ')
    line = r.sub(r'set \1 ', line)

    # NL natural log syntax
    r = re.compile(r'Log\[([^]]+)\]')
    line = r.sub(r'ln \1', line)

    # NL exp syntax
    r = re.compile(r'E\^\(')
    line = r.sub(r'e ^ (', line)

    # NL spacing requirements
    r = re.compile(r'([^ ])([*+/^-])')
    line = r.sub(r'\1 \2', line)
    r = re.compile(r'([*+/^-])([^ ])')
    line = r.sub(r'\1 \2', line)

    print line + "\n"

sys.exit(0)
