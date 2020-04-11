#! /usr/bin/env python3
# __main__.py

import os
import sys

from config import *
import board
import IO
import playmode
import readmode


# choosing mode
while True:
    print('R to read mode / P to play mode >>>', end=' ')
    ch = input()
    
    if ch in ['P', 'p']:
        playmode.playmode()
        break

    elif ch in ['R', 'r']:
        readmode.readmode()
        break