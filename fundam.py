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


if __name__=="__main__":
    try:
        print(PosNeg(int(input('Enter a posnegee '))))
    except:
        print('INVALID INPUT')
    try:
        print(InSize(int(input('Enter an InSizee '))))
    except:
        print('INVALID INPUT')