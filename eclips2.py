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

def eclips2_cmd(cmd):
    # kinda test mode - laser pointer is on, but offset from where it would cut
    #if cmd.startswith("PD"):
    #    cmd = "PU" + cmd[2:]

    dev.write(0x02, cmd)
    dev.read(0x82, 1)

def eclips2_init():
    # init?
    eclips2_cmd(";:H A L0 ECN U P1;US8;")

    print("Get ready for loading mat")
    input()

    eclips2_cmd("US5;")
    eclips2_cmd("PU600,0;")
    eclips2_cmd("!PG;")

    input()

    eclips2_cmd(";:H A L0 ECN U P1;US8;")
    eclips2_cmd("US7;")

def eclips2_end():
    # "done"?
    eclips2_cmd("PU;")
    eclips2_cmd("!PG;")
