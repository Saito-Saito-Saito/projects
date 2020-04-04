#! usr/bin/env python3
# csjudge.py

import copy

from config import *
import move
import fundfunc


def checkcounter(checkee, board=main_board):
    # searching for checkee's king
    for col in range(SIZE):
        if checkee * KING in board[col]:
            toCOL = col
            toROW = board[col].index(checkee * KING)
            break
    
    # if there is no king, the opponent cannot check
    try:
        toCOL = toCOL
    except:
        return 0

    # count up all the pieces that checks
    counter = 0
    for frCOL in range(SIZE):
        for frROW in range(SIZE):
            if fundfunc.PosNeg(board[frCOL][frROW]) == -checkee and move.motionjudge(frCOL, frROW, toCOL, toROW, QUEEN, board):
                counter += 1
    return counter


def checkmatejudge(matee, board=main_board):
    # if matee is not checked, it's not checkmate
    if checkcounter(matee, board) == 0:
        return False

    # searching for the move the matee can flee the check
    for frCOL in range(SIZE):
        for frROW in range(SIZE):
            if fundfunc.PosNeg(board[frCOL][frROW]) == matee:
                for toCOL in range(SIZE):
                    for toROW in range(SIZE):
                        local_board = copy.deepcopy(board)
                        if move.move(frCOL, frROW, toCOL, toROW, QUEEN, local_board) and checkcounter(matee, local_board) == 0:
                            logging.info('THERE IS {}, {} -> {}, {}'.format(frCOL,frROW,toCOL,toROW))
                            return False
    # completing all the loop, there is no way to flee the check
    return True


def stalematejudge(matee, board=main_board):
    # if checked, it's not stalemate
    if checkcounter(matee, board):
        return False

    # searching all the moves for one that can avoid check in moving
    for frCOL in range(SIZE):
        for frROW in range(SIZE):
            if fundfunc.PosNeg(board[frCOL][frROW]) == matee:
                for toCOL in range(SIZE):
                    for toROW in range(SIZE):
                        local_board=copy.deepcopy(board)
                        if move.move(frCOL, frROW, toCOL, toROW, QUEEN, local_board) and checkmatejudge(matee, local_board) == False:
                            logging.info('THERE IS {}, {} -> {}, {}'.format(frCOL, frROW, toCOL, toROW))
                            return False
    # completing the loop, there is no way to avoid check
    return True

