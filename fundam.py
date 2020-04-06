#! /usr/bin/env python3
# fundam.py

import config

def PosNeg(subject):
    if subject > 0:
        return 1
    elif subject < 0:
        return - 1
    else:
        return 0


def InSize(subject):
    if 0 <= subject < config.SIZE:
        return True
    else:
        return False
