import usb.core
import usb.util
import time

# find our device
dev = usb.core.find(idVendor=0x4348, idProduct=0x5537)

# was it found?
if dev is None:
    raise ValueError('Device not found')

# set the active configuration. With no arguments, the first
# configuration will be the active one
dev.set_configuration()

def cmd(cmd):
    # kinda test mode - laser pointer is on, but offset from where it would cut
    #if cmd.startswith("PD"):
    #    cmd = "PU" + cmd[2:]

    dev.write(0x02, cmd)
    dev.read(0x82, 1)

# init?
cmd(";:H A L0 ECN U P1;US8;")

print("Get ready for loading mat")
input()

cmd("US5;")
cmd("PU1344,0;")
cmd("US6;")
cmd("PU2368,0;")
cmd("PU320,0;")

time.sleep(3)

cmd("US7;")

with open("program.hpgl", "r") as file:
    program = file.read().split(";")

for entry in program:
    cmd(entry + ";")

# "done"?
cmd("!PG;")
