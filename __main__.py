#! /usr/bin/env python3
# __main__.py

import os
import sys

from config import *
import board
import IO


# file preparation
record = open('.\\record.txt', 'w')

# for recording
turn = 0


main_board = board.Board()
player = WHITE
main_board.BOARDprint()

while True:
    ### GAME SET JUDGE
    if main_board.king_place(player) == False:
        winner = -player
        break
    if main_board.checkmatejudge(player):
        print('CHECKMATE')
        winner = -player
        # break
    if main_board.stalematejudge(player):
        print('STALEMATE')
        winner = EMPTY
        break

    ### INPUT
    if player == WHITE:
        print('WHITE (X to givw up / H to help) >>> ', end='')
    elif player == BLACK:
        print('BLACK (X to givw up / H to help) >>> ', end='')
    else:
        logging.error('UNEXPECTED VALUE of PLAYER in while loop')
        print('SYSTEM ERROR')
        record.write('SYSTEM ERROR')
        winner = EMPTY
        break
    s = input()
    
    ### INPUT ANALYSIS
    # deleting all spaces
    s = s.replace(' ', '')
    # give up
    if s in ['X', 'x'] or (player == WHITE and s == '0-1') or (player == BLACK and s == '1-0'):
        winner = -player
        break
    # draw
    if s == '1/2-1/2':
        if player == WHITE:
            print('BLACK: Do you agree (y/n)? >>> ', end='')
        elif player == BLACK:
            print('WHITE: Do you agree (y/n)? >>> ', end='')
        else:
            logging.error('UNEXPECTED VALUE of PLAYER in while loop')
            print('SYSTEM ERROR')
            record.write('SYSTEM ERROR')
            winner = EMPTY
            break
        if input() in ['Y', 'y']:
            winner = EMPTY
            break
        else:
            continue
    # help
    if s in ['H', 'h']:
        IO.instruction()
        continue
    # format check
    s_record = s
    motion = main_board.s_analyze(s, player)
    # invalid input
    if motion == False or main_board.move(*motion) == False:
        print('INVALID INPUT/MOTION')
        continue

    ### PARAMETERS CONTROL
    piece = abs(main_board.board[motion[2]][motion[3]])
    # for e.p.
    if piece == PAWN and abs(motion[3] - motion[1]) > 1:
        main_board.ep_target = [motion[2], motion[3]]
    else:
        main_board.ep_target = [OVERSIZE, OVERSIZE]
    # for castling q-side
    if player in main_board.castl_q and (piece == KING or (piece == ROOK and motion[0] == a - 1)):
        main_board.castl_q.remove(player)
    # for castling k-side
    if player in main_board.castl_k and (piece == KING or (piece == ROOK and motion[0] == h - 1)):
        main_board.castl_k.remove(player)


    logging.info('ep = {}'.format(main_board.ep_target))
        

    main_board.BOARDprint()

    # recording the move
    if player == WHITE:
        record.write('{}\t'.format(turn + 1))
    elif player == BLACK:
        pass
    else:
        logging.error('UNEXPECTED VALUE of PLAYER in while loop')
        print('\tSYSTEM ERROR')
        record.write('SYSTEM ERROR')
        winner = EMPTY
        break

    record.write(s_record.ljust(12))
    if player == WHITE:
        pass
    elif player == BLACK:
        record.write('\n')
    else:
        record.write('SYSTEM ERROR')
        logging.error('UNEXPECTED VALUE of PLAYER in while loop')
        winner = EMPTY
        break

    # turn count
    if player == BLACK:
        turn += 1
    
    # player change
    player *= -1
    

print('\nGAME SET')
if winner == EMPTY:
    print('1/2 - 1/2\tDRAW')
    if player == WHITE:
        record.write('{}\t1/2-1/2'.format(turn + 1))
    else:
        record.write('1/2-1/2')
elif winner == WHITE:
    print('1 - 0\tWHITE WINS')
    record.write('1-0')
elif winner == BLACK:
    print('0 - 1\tBLACK WINS')
    record.write('{}\t0-1'.format(turn + 1))
else:
    logging.error('UNEXOECTED VALUE of PLAYER out of the loop')
    record.write('SYSTEM ERROR')
    print('SYSTEM ERROR')


record.close()


# record output
print('\nDo you want the record (y/n)? >>> ', end='')
if input() in ['y', 'Y']:
    record = open('.\\record.txt', 'r')
    print('\n------------------------------------')
    print(record.read())
    print('------------------------------------')
    record.close()


print('\nGAME OVER\n')
