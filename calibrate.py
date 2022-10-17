import time
import curses
from eclips2 import eclips2_cmd, eclips2_init, eclips2_end

hpgl_inch_factor = 1016
hpgl_mm_factor   = 40

lower_right = (0,                       0)
lower_left  = (0,                       297 * hpgl_mm_factor)
upper_right = (210 * hpgl_mm_factor,    0)
upper_left  = (210 * hpgl_mm_factor,    297 * hpgl_mm_factor)

eclips2_init()
eclips2_cmd("PU0,0;")

current_pos = (0, 0)

def absolute(pos):
    eclips2_cmd("PU{},{};".format(pos[0], pos[1]))

def move(x, y):
    global current_pos
    current_pos = (current_pos[0] + x, current_pos[1] + y)
    absolute(current_pos)
    time.sleep(0.1)

def calibration_check(pos):
    absolute((pos[0] + current_pos[0], pos[1] + current_pos[1]))
    while stdscr.getkey() != "\n":
        None

def calibration_verify(pos):
    eclips2_cmd("PD{},{};".format(pos[0] + current_pos[0], pos[1] + current_pos[1]))

stdscr = curses.initscr()
curses.noecho()
curses.cbreak()
stdscr.keypad(True)

stdscr.addstr(
    "Move head to start position, using the following keys\n"
    " * HJKL for fast movements\n"
    " * hjkl for slower movement\n"
    " * arrow keys for exact movement\n"
    " * <space> to slam pen down until you press another key\n"
    "Be careful not to navigate past the stops, it will ignore commands after that\n\n"
)

while True:
    while True:
        stdscr.addstr(8, 0, "X = {}, Y = {}         \n".format(current_pos[0], current_pos[1]))

        cmd = stdscr.getkey()
        factor=100

        if cmd.startswith("KEY_"):
            factor=1
            if cmd == "KEY_LEFT":
                cmd = "h"
            elif cmd == "KEY_RIGHT":
                cmd = "l"
            elif cmd == "KEY_UP":
                cmd = "k"
            elif cmd == "KEY_DOWN":
                cmd = "j"
        elif cmd.isupper():
            factor*=10
            cmd = cmd.lower()

        if cmd == "h":
            move(0, factor)
        elif cmd == "j":
            move(factor, 0)
        elif cmd == "k":
            move(-factor, 0)
        elif cmd == "l":
            move(0, -factor)
        elif cmd == " ":
            eclips2_cmd("PD{},{};".format(current_pos[0], current_pos[1]))
            time.sleep(0.5)
            eclips2_cmd("PU{},{};".format(current_pos[0], current_pos[1]))
        elif cmd == "\n":
            break

    stdscr.addstr("Calibration done? [yn]\n")
    if stdscr.getkey().lower() == "y":
        stdscr.addstr("Going to upper left\n")
        calibration_check(upper_left)

        stdscr.addstr("Going to lower left\"\n")
        calibration_check(lower_left)

        stdscr.addstr("Going to upper right\n")
        calibration_check(upper_right)

        stdscr.addstr("Going to lower right\n")
        calibration_check(lower_right)

    stdscr.addstr("Another pass? [yn]\n")
    if stdscr.getkey().lower() != "y":
        break

absolute((0, 0))

stdscr.addstr("Draw verification piece? [yn]\n")
if stdscr.getkey().lower() == "y":
        calibration_verify(lower_right)
        calibration_verify(lower_left)
        calibration_verify(upper_left)
        calibration_verify(upper_right)
        calibration_verify(lower_right)
        calibration_verify(upper_left)
        calibration_verify(upper_right)
        calibration_verify(lower_left)

absolute((0, 0))

eclips2_end()

curses.nocbreak()
stdscr.keypad(False)
curses.echo()
curses.endwin()

print("Your calibration values are X={}, Y={}\n".format(current_pos[0], current_pos[1]))
