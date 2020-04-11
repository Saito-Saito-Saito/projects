#! /usr/bin/env python3
# __main__.py

import os
import sys

from config import *
import board
import IO


# new file preparation
record = open(MAINRECADDRESS, 'w')
record.close()
record = open(SUBRECADDRESS, 'w')
record.close()

main_board = board.Board()
main_board.BOARDprint()

while True:
    ### GAME SET JUDGE
    if main_board.king_place(main_board.player) == False:
        winner = -main_board.player
        break
    if main_board.checkmatejudge(main_board.player):
        print('CHECKMATE')
        winner = -main_board.player
        # break
    if main_board.stalematejudge(main_board.player):
        print('STALEMATE')
        winner = EMPTY
        break

    ### INPUT
    if main_board.player == WHITE:
        print('WHITE (X to givw up / H to help / Z to back) >>> ', end='')
    elif main_board.player == BLACK:
        print('BLACK (X to givw up / H to help / Z to back) >>> ', end='')
    else:
        logging.error('UNEXPECTED VALUE of PLAYER in while loop')
        print('SYSTEM ERROR')
        sys.exit()
    s = input()
    
    ### INPUT ANALYSIS
    # deleting all spaces
    s = s.replace(' ', '')
    # give up
    if s in ['X', 'x'] or (main_board.player == WHITE and s == '0-1') or (main_board.player == BLACK and s == '1-0'):
        winner = -main_board.player
        break
    # draw
    if s == '1/2-1/2':
        if main_board.player == WHITE:
            print('BLACK: Do you agree (y/n)? >>> ', end='')
        elif main_board.player == BLACK:
            print('WHITE: Do you agree (y/n)? >>> ', end='')
        else:
            logging.error('UNEXPECTED VALUE of PLAYER in while loop')
            print('SYSTEM ERROR')
            sys.exit()
        if input() in ['Y', 'y']:
            winner = EMPTY
            break
        else:
            continue
    # help
    if s in ['H', 'h']:
        IO.instruction()
        continue
    # back
    if s in ['Z', 'z']:
        if main_board.player == WHITE:
            print('Do you agree, BLACK (y/n)? >>> ', end='')
        elif main_board.player == BLACK:
            print('Do you agree, WHITE (y/n) >>> ', end='')
        else:
            logging.error('UNEXPECTED VALUE of PLAYER in the while loop')
            sys.exit()
        if input() not in ['y', 'Y']:
            continue
        new_board = main_board.tracefile(main_board.turn - 1, main_board.player)
        if new_board == main_board:
            logging.warning('IMPOSSIBLE TO BACK')
            print('SORRY, NOW WE CANNOT BACK THE BOARD')
        else:
            main_board = new_board
            main_board.BOARDprint()
        continue
    # format check
    s_record = s.replace('o', 'O')
    # motion detection
    motion = main_board.s_analyze(s)
    # invalid input
    if motion == False or main_board.move(*motion) == False:
        print('INVALID INPUT/MOTION')
        continue

    # board output
    main_board.BOARDprint()

    # recording the move
    main_board.record(s_record, MAINRECADDRESS)
    
    

print('\nGAME SET')
if winner == EMPTY:
    # for record
    main_board.player *= -1
    print('1/2 - 1/2\tDRAW')
    main_board.record('1/2-1/2', MAINRECADDRESS)
elif winner == WHITE:
    print('1 - 0\tWHITE WINS')
    main_board.record('1-0', MAINRECADDRESS) # after white's move, 1-0 is written where black's move is written
elif winner == BLACK:
    print('0 - 1\tBLACK WINS')
    main_board.record('0-1', MAINRECADDRESS) # after white's move, 1-0 is written where black's move is written
else:
    logging.error('UNEXOECTED VALUE of PLAYER out of the loop')
    print('SYSTEM ERROR')
    sys.exit()


# record output
print('\nDo you want the record (y/n)? >>> ', end='')
if input() in ['y', 'Y']:
    record = open(MAINRECADDRESS, 'r')
    print('\n------------------------------------')
    print(record.read())
    print('------------------------------------')
    record.close()


print('\nGAME OVER\n')
