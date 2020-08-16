#! usr/bin/env/ Python3
# print.py
# coded by Saito-Saito-Saito
# explained on https://Saito-Saito-Saito.github.io/chess
# last updated: 16 August 2020
# NOTE: This code is only for explaining, so is not neccessary to run.

from board import *

class BoardPrint(Board):
    def PrintWhiteSide(self):
        '''
        a   b   c   d   e   f   g   h
       -------------------------------
    8 | ♖ | ♘ | ♗ | ♕ | ♔ | ♗ | ♘ | ♖ | 8
       -------------------------------
    7 | ♙ | ♙ | ♙ | ♙ | ♙ | ♙ | ♙ | ♙ | 7
       -------------------------------
    6 |   |   |   |   |   |   |   |   | 6
       -------------------------------
    5 |   |   |   |   |   |   |   |   | 5
       -------------------------------
    4 |   |   |   |   |   |   |   |   | 4
       -------------------------------
    3 |   |   |   |   |   |   |   |   | 3
       -------------------------------
    2 | ♟ | ♟ | ♟ | ♟ | ♟ | ♟ | ♟ | ♟ | 2
       -------------------------------
    1 | ♜ | ♞ | ♝ | ♛ | ♚ | ♝ | ♞ | ♜ | 1
       -------------------------------
        a   b   c   d   e   f   g   h
        '''
        print('\n') # spacing
        print('\t    a   b   c   d   e   f   g   h')    # the top file index
        print('\t   -------------------------------')   # border
        for rank in range(SIZE - 1, -1, -1):  # down to less
            print('\t{} |'.format(rank + 1), end='')    # rank index and border
            for file in range(SIZE):
                print(' {} |'.format(IO.ToggleType(self.board[file][rank])), end='')    # piece and border
            print(' {}'.format(rank + 1))   # rank index
            print('\t   -------------------------------')   # border
        print('\t    a   b   c   d   e   f   g   h')    # file index
        print('\n') # spacing
    

if __name__ == "__main__":
    test_board = BoardPrint()
    test_board.PrintWhiteSide()
