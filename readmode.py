#! /usr/bin/env python3
# readmode.py

import sys

from config import *
import board

def readmode():
    print('ENTER TO START')
    input()
    main_board = board.Board()
    
    while True:
        if main_board.player == WHITE:
            print('{}\tWHITE'.format(main_board.turn), end='\t')
            new_board = main_board.tracefile(main_board.turn, BLACK, False)
        elif main_board.player == BLACK:
            print('{}\tBLACK'.format(main_board.turn), end='\t')
            new_board = main_board.tracefile(main_board.turn + 1, WHITE, False)
        else:
            logging.error('UNEXPECTED VALUE of PLAYER in readmode')
            print('SYSTEM ERROR')
            sys.exit()

        if type(new_board) is bool:
            print('NO WAY TO CONTINUE')
            return
        elif type(new_board) is int:
            if new_board == EMPTY:
                print('1/2-1/2\nDRAW')
                return
            elif new_board == WHITE:
                print('1-0\nWHITE WINS')
                return
            elif new_board == BLACK:
                print('0-1\nBLACK WINS')
                return
            else:
                logging.error('UNEXPECTED VALUE of new_board in readmode')
                print('SYSTEM ERROR')
                sys.exit()
        else:
            main_board = new_board
            print(main_board.s)
            main_board.BOARDprint()

        print('ENTER TO NEXT / X TO QUIT ', end='')
        if input() in ['X', 'x']:
            print('QUITTED')
            return