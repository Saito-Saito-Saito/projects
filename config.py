#! /usr/bin/env python3
# config.py
# programmed by Saito-Saito-Saito
# explained on https://saito-saito-saito.github.io/chess
# last update: 28/4/2020



import logging

logging.basicConfig(level=logging.CRITICAL, format='%(levelname)s - %(filename)s - L%(lineno)d - %(message)s')

# record files
MAINRECADDRESS = 'mainrecord.txt'
SUBRECADDRESS = 'subrecord.txt'

# board size
SIZE = 8
# for if switches
OVERSIZE = SIZE * SIZE

# for index
FILE = 0
RANK = 1
a, b, c, d, e, f, g, h = 1, 2, 3, 4, 5, 6, 7, 8

EMPTY = 0
P = PAWN = 1
R = ROOK = 2
N = KNIGHT = 3
B = BISHOP = 4
Q = QUEEN = 5
K = KING = 6

WHITE = 1
BLACK = -1
