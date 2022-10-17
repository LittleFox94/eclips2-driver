import re
from eclips2 import eclips2_cmd, eclips2_init, eclips2_end

eclips2_init()

with open("program.hpgl", "r") as file:
    program = file.read().split(";")

for entry in program:
    matches = re.search("(\\w{2})([.\-0-9]+),([.\-0-9]+)", entry)
    if matches:
        coords = (
            int(matches.group(2)) + 820,#940
            int(matches.group(3)) + 870,#1040,
        )

        entry = "{}{},{}".format(matches.group(1), coords[0], coords[1])

    eclips2_cmd(entry + ";")

eclips2_end()
