#! usr/bin/env python3
# config.py


import logging

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - L%(lineno)d - %(message)s')

# board size (8 * 8)
SIZE = 8
OVERSIZE = SIZE * SIZE

# players
WHITE = 1
BLACK = -1

# pieces
EMPTY = 0
P = PAWN = 1
R = ROOK = 2
N = KNIGHT = 3
B = BISHOP = 4
Q = QUEEN = 5
K = KING = 6

# rows & columns
COL = 0
ROW = 1
a, b, c, d, e, f, g, h = 1, 2, 3, 4, 5, 6, 7, 8

# main board
main_board = [
    [R, P, 0, 0, 0, 0, -P, -R],
    [N, P, 0, 0, 0, 0, -P, -N],
    [B, P, 0, 0, 0, 0, -P, -B],
    [Q, P, 0, 0, 0, 0, -P, -Q],
    [K, P, 0, 0, 0, 0, -P, -K],
    [B, P, 0, 0, 0, 0, -P, -B],
    [N, P, 0, 0, 0, 0, -P, -N],
    [R, P, 0, 0, 0, 0, -P, -R]
]

# var for en passant; record the square to which a pawn has come by two steps forward
ep_target = [OVERSIZE, OVERSIZE]
# var for castling; who can do castling yet
castl_k = [WHITE, BLACK]
castl_q = [WHITE, BLACK]

