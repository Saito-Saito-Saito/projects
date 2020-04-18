#! /usr/bin/env python3
# config.py


import logging

logging.basicConfig(level=logging.CRITICAL, format='%(levelname)s - %(filename)s - L%(lineno)d - %(message)s')

# records
MAINRECADDRESS = 'mainrecord.txt'
SUBRECADDRESS = 'subrecord.txt'

SIZE = 8
OVERSIZE = SIZE * SIZE

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
