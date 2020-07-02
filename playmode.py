#! /usr/bin/env python3
# playmode.py
# programmed by Saito-Saito-Saito
# explained on https://Saito-Saito-Saito.github.io/chess
# last update: 2/7/2020


import sys

from config import *
import board
import IO

local_logger = setLogger(__name__)


def playmode(logger=None):
    # logger setup
    logger = logger or local_logger
    
    # new file preparation
    record = open(MAINRECADDRESS, 'w')
    record.close()
    record = open(SUBRECADDRESS, 'w')
    record.close()

    # initializing the board
    main_board = board.Board()
    main_board.BOARDprint()

    while True:
        ### GAME SET JUDGE
        # king captured
        if main_board.king_place(main_board.player) == False:
            winner = -main_board.player
            break
        # checkmate
        if main_board.checkmatejudge(main_board.player):
            print('CHECKMATE')
            winner = -main_board.player
            # break
        # stalemate
        if main_board.stalematejudge(main_board.player):
            print('STALEMATE')
            winner = EMPTY  # stalemate is draw
            break

        ### PLAYER INTRODUCTION
        if main_board.player == WHITE:
            print('WHITE (X to resign / H to help / Z to back) >>> ', end='')
        elif main_board.player == BLACK:
            print('BLACK (X to resign / H to help / Z to back) >>> ', end='')
        else:
            logger.error('UNEXPECTED VALUE of PLAYER in while loop')
            print('SYSTEM ERROR')
            sys.exit()

        ### INPUT ANALYSIS
        # inputting and deleting all spaces, replacing 'o' into 'O'
        main_board.s = input().replace(' ', '').replace('o', 'O')
        # resign code
        if main_board.s in ['X', 'x']:
            winner = -main_board.player
            break
        # help code
        if main_board.s in ['H', 'h']:
            IO.instruction()
            continue
        # back code
        if main_board.s in ['Z', 'z']:
            # necessary for the opponent to allow the player to back
            if main_board.player == WHITE:
                print('Do you agree, BLACK (y/n)? >>> ', end='')
            elif main_board.player == BLACK:
                print('Do you agree, WHITE (y/n) >>> ', end='')
            else:
                logger.error('UNEXPECTED VALUE of PLAYER in the while loop')
                sys.exit()
            # in case rejected
            if input() not in ['y', 'Y', 'Yes', 'YES', 'yes']:
                continue
            # in case allowed
            new_board = main_board.tracefile(main_board.turn - 1, main_board.player, True)
            # unavailable to back
            if new_board == main_board:
                logger.warning('IMPOSSIBLE TO BACK')
                print('SORRY, NOW WE CANNOT BACK THE BOARD')
            # available to back
            else:
                main_board = new_board
                main_board.BOARDprint()
            continue
        # motion detection
        motion = main_board.s_analyze()
        # game set (resign)
        if type(motion) is int:
            if motion == EMPTY:
                # necessary to agree to end the game
                if main_board.player == WHITE:
                    print('Do you agree, BLACK (y/n)? >>>', end=' ')
                elif main_board.player == BLACK:
                    print('Do you agree, WHITE (y/n)? >>>', end=' ')
                else:
                    logger.error('UNEXPECTED VALUE of PLAYER in the while loop')
                    print('SYSTEM ERROR')
                    sys.exit()
                # when agreed
                if input() in ['y', 'Y']:
                    winner = EMPTY
                    break
                # when rejected
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
        # invalid input (here, valid motion is conducted)
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
        logger.error('UNEXPECTED VALUE of PLAYER out of the loop')
        print('SYSTEM ERROR')
        sys.exit()


    # record output
    if input('\nDo you want the record (y/n)? >>> ') in ['y', 'Y', 'yes', 'YES', 'Yes']:
        record = open(MAINRECADDRESS, 'r')
        print('\n------------------------------------')
        print(record.read())
        print('------------------------------------')
        record.close()


    print('\nGAME OVER\n')


if __name__=="__main__":
    playmode()
    