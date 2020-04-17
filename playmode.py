#! /usr/bin/env python3
# playmode.py

import sys

from config import *
import board
import IO

def playmode():
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

        ### INPUT ANALYSIS
        # deleting all spaces
        main_board.s = input().replace(' ', '').replace('o', 'O')
        # give up
        if main_board.s in ['X', 'x']:
            winner = -main_board.player
            break
        # help
        if main_board.s in ['H', 'h']:
            IO.instruction()
            continue
        # back
        if main_board.s in ['Z', 'z']:
            if main_board.player == WHITE:
                print('Do you agree, BLACK (y/n)? >>> ', end='')
            elif main_board.player == BLACK:
                print('Do you agree, WHITE (y/n) >>> ', end='')
            else:
                logging.error('UNEXPECTED VALUE of PLAYER in the while loop')
                sys.exit()
            if input() not in ['y', 'Y']:
                continue
            new_board = main_board.tracefile(
                main_board.turn - 1, main_board.player)
            if new_board == main_board:
                logging.warning('IMPOSSIBLE TO BACK')
                print('SORRY, NOW WE CANNOT BACK THE BOARD')
            else:
                main_board = new_board
                main_board.BOARDprint()
            continue
        # motion detection
        motion = main_board.s_analyze()
        # game set
        if type(motion) is int:
            if motion == EMPTY:
                if main_board.player == WHITE:
                    print('Do you agree, BLACK (y/n)? >>>', end=' ')
                elif main_board.player == BLACK:
                    print('Do you agree, WHITE (y/n)? >>>', end=' ')
                else:
                    logging.error('UNEXPECTED VALUE of PLAYER in the while loop')
                    print('SYSTEM ERROR')
                    sys.exit()
                if input() in ['y', 'Y']:
                    winner = EMPTY
                    break
                else:
                    continue
            elif motion == WHITE == -main_board.player:
                winner = WHITE
                break
            elif motion == BLACK == -main_board.player:
                winner = BLACK
                break
            else:
                print('IVNALID INPUT')
                continue
        # invalid input
        if motion == False or main_board.move(*motion) == False:
            print('INVALID INPUT/MOTION')
            continue

        # board output
        main_board.BOARDprint()

        # recording the move
        main_board.record(MAINRECADDRESS)


    print('\nGAME SET')
    if winner == EMPTY:
        # for record
        main_board.player *= -1
        print('1/2 - 1/2\tDRAW')
        main_board.s = '1/2-1/2 '
        main_board.record(MAINRECADDRESS)
    elif winner == WHITE:
        print('1 - 0\tWHITE WINS')
        # after white's move, 1-0 is written where black's move is written
        main_board.s = '1-0 '
        main_board.record(MAINRECADDRESS)
    elif winner == BLACK:
        print('0 - 1\tBLACK WINS')
        # after white's move, 1-0 is written where black's move is written
        main_board.s = '0-1 '
        main_board.record(MAINRECADDRESS)
    else:
        logging.error('UNEXPECTED VALUE of PLAYER out of the loop')
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