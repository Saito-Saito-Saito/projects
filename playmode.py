#! /usr/bin/env python3
# playmode.py
# programmed by Saito-Saito-Saito
# explained on https://Saito-Saito-Saito.github.io/chess
# last updated: 15 August 2020


import sys

from config import *
import board
import IO

local_logger = setLogger(__name__)


def playmode(turnmode=True, logger=None):
    # logger setup
    logger = logger or local_logger
    
    # new file preparation
    record = open(MAINRECADDRESS, 'w')
    record.close()
    record = open(SUBRECADDRESS, 'w')
    record.close()

    # initializing the board
    main_board = board.Board()
    main_board.print(turnmode=turnmode)

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
            break
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
            sys.exit('SYSTEM ERROR')

        ### INPUT ANALYSIS
        # inputting and deleting all spaces, replacing 'o' into 'O'
        main_board.s = input().replace(' ', '').replace('o', 'O')
        # help code
        if main_board.s in ['H', 'h']:
            IO.instruction()
            main_board.print(turnmode=turnmode, reverse=False)
            continue
        # resign code
        if main_board.s in ['X', 'x']:
            winner = -main_board.player
            break
        # back code
        if main_board.s in ['Z', 'z']:
            # necessary for the opponent to allow the player to back
            if main_board.player == WHITE:
                print('Do you agree, BLACK (y/n)? >>> ', end='')
            elif main_board.player == BLACK:
                print('Do you agree, WHITE (y/n) >>> ', end='')
            else:
                logger.error('UNEXPECTED VALUE of PLAYER in the while loop')
                sys.exit('SYSTEM ERROR')
            # in case rejected
            if input() not in ['y', 'Y', 'Yes', 'YES', 'yes']:
                continue
            # in case allowed
            new_board = main_board.tracefile(main_board.turn - 1, main_board.player, isrecwrite=True)
            # unavailable to back
            if new_board == main_board:
                logger.warning('IMPOSSIBLE TO BACK')
                print('SORRY, NOW WE CANNOT BACK THE BOARD')
            # available to back
            else:
                main_board = new_board
                main_board.print(turnmode=turnmode)
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
                    sys.exit('SYSTEM ERROR')
                # when agreed
                if input() in ['y', 'Y']:
                    winner = EMPTY
                    break
                # when rejected
                else:
                    main_board.print(turnmode=turnmode, reverse=False)
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

        # recording the move
        main_board.record(MAINRECADDRESS)

        # turn count
        if main_board.player == BLACK:
            main_board.turn += 1

        # player change
        main_board.player *= -1
        
        # board output
        main_board.print(turnmode=turnmode)



    print('\nGAME SET')
    if winner == EMPTY:
        print('1/2 - 1/2\tDRAW')
        # for record
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
        sys.exit('SYSTEM ERROR')


    # record output
    if input('\nDo you want the record (y/n)? >>> ') in ['y', 'Y', 'yes', 'YES', 'Yes']:
        record = open(MAINRECADDRESS, 'r')
        print('\n------------------------------------')
        print(record.read())
        print('------------------------------------')
        record.close()


    print('\nGAME OVER\n')


if __name__ == "__main__":
    playmode()
    