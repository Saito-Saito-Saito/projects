#! /usr/bin/env python3
# main.py

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