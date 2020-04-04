#! usr/bin/env python3
# fundfunc.py


import config

# useful to judge the player
def PosNeg(subject):
    if subject > 0:
        return 1
    elif subject < 0:
        return - 1
    else:
        return 0

# useful to judge whether it's in the board
def InBoard(subject):
    if 0 <= subject < config.SIZE:
        return True
    else:
        return False

