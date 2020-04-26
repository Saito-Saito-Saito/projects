#! /usr/bin/env python3
# main.py 
# programmed by Saito-Saito-Saito
# explained on https://saito-saito-saito.github.io/chess
# last update: 28/4/2020

import playmode
import readmode


# choosing mode
while True:
    print('R to read mode / P to play mode >>>', end=' ')
    ch = input()
    
    if ch in ['P', 'p' 'play', 'PLAY', 'Play']:
        playmode.playmode()
        break

    elif ch in ['R', 'r', 'READ', 'read', 'Read']:
        readmode.readmode()
        break