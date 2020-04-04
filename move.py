#! usr/bin/env python3
# move.py


from config import *
from fundfunc import *


def motionjudge(frCOL, frROW, toCOL, toROW, promote=EMPTY, board=main_board):
    # in case out of the board
    if not (InBoard(frCOL) and InBoard(frROW) and InBoard(toCOL) and InBoard(toROW)):
        logging.debug('OUT OF THE BOARD')
        return False

    player = PosNeg(board[frCOL][frROW])
    piece = abs(board[frCOL][frROW])
    
    # if moving EMPTY
    if piece == EMPTY:
        logging.debug('MOVING EMPTY')
        return False
    
    # there is already another piece where the player is moving the piece to
    if PosNeg(board[toCOL][toROW]) == player:
        logging.debug('THERE IS ALREADY ANOTHER OWN PIECE')
        return False

    # PAWN
    if piece == PAWN:
        # not promoting on the edge
        if abs(promote) not in [Q, R, B, N] and ((player == WHITE and toROW == 8 - 1) or (player == BLACK and toROW == 1 - 1)):
            logging.debug('NECESSARY TO PROMOTE')
            return False
        # normal motion (one step forward); the same COL, one step forward, TO is empty
        # NOTE: if player is WHITE, the pawn has to move as the row number increases
        if frCOL == toCOL and toROW - frROW == player and board[toCOL][toROW] == EMPTY:
            return True
        # normal capturing; next COL, one step forward, TO is opponent's
        if abs(toCOL - frCOL) == 1 and toROW - frROW == player and PosNeg(board[toCOL][toROW]) == -player:
            return True
        # first two steps; the same COL, two steps forward, passing squares are empty
        if frCOL == toCOL and toROW - frROW == 2 * player and board[frCOL][frROW + player] == board[toCOL][toROW] == EMPTY:
            return True
        # en passant; FR - ep_target. TO - ep_target, TO is empty
        if abs(ep_target[COL] - frCOL) == 1 and ep_target[ROW] == frROW and ep_target[COL] == toCOL and toROW - ep_target[ROW] == player and board[toCOL][toROW] == EMPTY:
            return True
        # all other moves are invalid
        logging.debug('INVALID PAWN MOTION')
        logging.info('ep_target = {}'.format(ep_target))
        return False

    # ROOK
    elif piece == ROOK:
        # invalid motion; different COL and ROW
        if frCOL != toCOL and frROW != toROW:
            logging.debug('INVALID ROOK MOTION')
            return False
        # else, you have to check whether there is an obstacle in the way

    # KNIGHT
    elif piece == KNIGHT:
        # valid motion
        if (abs(toCOL - frCOL) == 1 and abs(toROW - frROW) == 2) or (abs(toCOL - frCOL) == 2 and abs(toROW - frROW) == 1):
            return True
        else:
            logging.debug('INVALID KNIGHT MOTION')
            return False

    # BISHOP
    elif piece == BISHOP:
        # invalid motion
        if abs(toCOL - frCOL) != abs(toROW - frROW):
            logging.debug('INVALID BISHOP MOTION')
            return False
        # else, you have to check whether there is an obstacle in the way

    # QUEEN
    elif piece == QUEEN:
        # invalid motion (cf. R & B)
        if frCOL != toCOL and frROW != toROW and abs(toCOL - frCOL) != abs(toROW - frROW):
            logging.debug('INVALID QUEEN MOTION')
            return False

    # KING
    elif piece == KING:
        # normal one step
        if abs(toCOL - frCOL) <= 1 and abs(toROW - frROW) <= 1:
            return True
        # preparation for checking castling 
        if player == WHITE:
            row = 1 - 1
        elif player == BLACK:
            row = 8 - 1
        else:
            logging.critical('UNEXPECTED PLAYER VALUE in motionjudge')
            return False
        # Q-side
        if player in castl_q and frCOL == e - 1 and toCOL == c - 1 and frROW == toROW == row and board[b - 1][row] == board[c - 1][row] == board[d - 1][row] == EMPTY:
            return True
        # K-side
        if player in castl_k and frCOL == e - 1 and toCOL == g - 1 and frROW == toROW == row and board[f - 1][row] == board[g - 1][row] == EMPTY:
            return True
        # all other moves are invalid
        logging.debug('INVALID KING MOTION')
        return False

    # unexpected kind of piece
    else:
        logging.critical('UNEXPECTED PIECE VALUE in motionjudge')
        return False

    # searching for an obstacle in the way of R/B/Q
    direction = [PosNeg(toCOL - frCOL), PosNeg(toROW - frROW)]
    focused = [frCOL + direction[COL], frROW + direction[ROW]]
    while focused[COL] != toCOL and focused[ROW] != toROW:
        if not (InBoard(focused[COL] and InBoard(focused[ROW]))):
            break
        if board[focused[COL]][focused[ROW]] != EMPTY:
            logging.debug('THERE IS AN OBSTACLE IN THE WAY')
            return False
        focused[COL] += direction[COL]
        focused[ROW] += direction[ROW]

    # there is no obstacle 
    return True


def move(frCOL, frROW, toCOL, toROW, promote=EMPTY, board=main_board):
    # invalid motion
    if motionjudge(frCOL, frROW, toCOL, toROW, promote, board) == False:
        return False

    player = PosNeg(board[frCOL][frROW])
    piece = abs(board[frCOL][frROW])
    
    # castling
    if piece == KING and abs(toCOL - frCOL) > 1:
        if player == WHITE:
            row = 1 - 1
        elif player == BLACK:
            row = 8 - 1
        else:
            logging.critical('UNEXPECTED PLAYER VALUE in Move')
            return False
        # Q-side
        if toCOL == c - 1:
            # moving ROOK
            board[d - 1][row] = board[a - 1][row]
            board[a - 1][row] = EMPTY
        elif toCOL == g - 1:
            # moving ROOK
            board[f - 1][row] = board[h - 1][row]
            board[h - 1][row] = EMPTY
        # king is to move later

    # en passant
    if piece == PAWN and frCOL != toCOL and board[toCOL][toROW] == EMPTY:
        # capturing opponent's pawn
        board[toCOL][frROW] = EMPTY
        # own pawn is to move later

    # promotion
    if piece == PAWN and (toROW == 1 - 1 or toROW == 8 - 1):
        # change the pawn into promote
        board[frCOL][frROW] = player * promote
        # move this later

    # move the piece
    board[toCOL][toROW] = board[frCOL][frROW]
    board[frCOL][frROW] = EMPTY
    return True

