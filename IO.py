#! usr/bin/env python3
# IO.py


import re
import copy

from config import *
import fundfunc
import move
import csjudge


def TypeChange(target):
    # piece ID -> piece letter
    if type(target) is int:
        if target == EMPTY:
            return ' '
        elif target == P * WHITE:
            return '♙'
        elif target == R * WHITE:
            return '♖'
        elif target == N * WHITE:
            return '♘'
        elif target == B * WHITE:
            return '♗'
        elif target == Q * WHITE:
            return '♕'
        elif target == K * WHITE:
            return '♔'
        elif target == P * BLACK:
            return '♟'
        elif target == R * BLACK:
            return '♜'
        elif target == N * BLACK:
            return '♞'
        elif target == B * BLACK:
            return '♝'
        elif target == Q * BLACK:
            return '♛'
        elif target == K * BLACK:
            return '♚'
        else:
            logging.critical('UNEXPECTED INPUT VALUE of A PIECE into TypeChange')
            return False

    # str, chr -> int
    elif type(target) is str or type(target) is chr:
        # a number
        if target.isdecimal():
            return int(target)
        # the kind of piece
        elif target == 'P':
            return P
        elif target == 'R':
            return R
        elif target == 'N':
            return N
        elif target == 'B':
            return B
        elif target == 'Q':
            return Q
        elif target == 'K':
            return K
        # row id
        elif ord('a') <= ord(target) <= ord('h'):
            return ord(target) - ord('a') + 1
        else:
            logging.critical('UNEXPECTED INPUT into TypeChange')
            return False

    # unexpected type
    else:
        logging.critical('UNEXPECTED INPUT TYPE into TypeChange')
        return False


def BoardPrint(board=main_board):
    print('\n')
    print('\t    a   b   c   d   e   f   g   h')
    print('\t   -------------------------------')
    for row in range(SIZE - 1, -1, -1):
        print('\t{} |'.format(row + 1), end='')
        for col in range(SIZE):
            print(' {} |'.format(TypeChange(board[col][row])), end='')
        print(' {}'.format(row + 1))
        print('\t   -------------------------------')
    print('\t    a   b   c   d   e   f   g   h')
    print('\n')
    

def s_analyze(s, player, board=main_board):
    # avoiding bugs
    if len(s) == 0:
        return False

    # deleting all of !?+-= at the tail
    while s[-1] in ['!', '?', '+', '-', '=']:
        del s[-1]

    # avoiding bugs
    if len(s) == 0:
        return False

    # matching the normal format
    match = re.match(r'^[PRNBQK]?[a-h]?[1-8]?[x]?[a-h][1-8](=[RNBQ]|e.p.)?[\+#]?$', s)
    
    if match:
        line = match.group()
        logging.info('line = {}'.format(line))

        # what piece is moving
        if line[0] in ['R', 'N', 'B', 'Q', 'K']:
            piece = TypeChange(line[0])
            line = line.lstrip(line[0])
        else:
            piece = PAWN
            
        # written info of what row the piece comes from
        if line[0].isdecimal():
            frCOL = OVERSIZE
            frROW = TypeChange(line[0]) - 1
            line = line.lstrip(line[0])
        # written info of what col the piecce comes from
        elif ord('a') <= ord(line[0]) <= ord('h') and ord('a') <= ord(line[1]) <= ord('x'):
            frCOL = TypeChange(line[0]) - 1
            frROW = OVERSIZE
            line = line.lstrip(line[0])
        # nothing is written about where the piece comes from
        else:
            frCOL = OVERSIZE
            frROW = OVERSIZE

        # whether the piece has captured one of the opponent's pieces
        if line[0] == 'x':
            CAPTURED = True
            line = line.lstrip(line[0])
        else:
            CAPTURED = False

        # where the piece goes to
        toCOL = TypeChange(line[0]) - 1
        toROW = TypeChange(line[1]) - 1

        # promotion
        if '=' in line:
            promote = line[line.index('=') + 1]
        else:
            promote = EMPTY
        
        # raising up all the available candidates
        candidates = []
        for col in range(SIZE):
            # when frCOL is written
            if fundfunc.InBoard(frCOL) and frCOL != col:
                continue
            
            for row in range(SIZE):
                # when frROW is written
                if fundfunc.InBoard(frROW) and frROW != row:
                    continue
                
                # piece
                if board[col][row] != player * piece:
                    continue

                # available motion
                if move.motionjudge(col, row, toCOL, toROW, promote) == False:
                    continue

                candidates.append([col, row])
                
        # checking all the candidates
        for reference in range(len(candidates)):
            local_board = copy.deepcopy(board)
            move.move(candidates[reference][COL], candidates[reference][ROW], toCOL, toROW, promote, local_board)
                        
            # capture; searching for the opponent's piece that has disappeared
            if CAPTURED or 'e.p.' in line:
                for col in range(SIZE):
                    for row in range(SIZE):
                        if fundfunc.PosNeg(board[col][row]) == -player and fundfunc.PosNeg(local_board[col][row]) != -player:
                            break
                    else:
                        continue
                    break
                else:
                    # it does not capture any piece
                    del candidates[reference]
                    reference -= 1
                    continue

            # check
            if line.count('+') > csjudge.checkcounter(player, local_board):
                del candidates[reference]
                reference -= 1
                continue

            # checkmate
            if '#' in line and csjudge.checkmatejudge(player, local_board) == False:
                del candidates[reference]
                reference -= 1
                continue

            # en passant
            if 'e.p.' in line and board[toCOL][toROW] != EMPTY:
                del candidates[reference]
                reference -= 1
                continue

        # return
        if len(candidates) == 1:
            return [candidates[0][COL], candidates[0][ROW], toCOL, toROW, promote]
        elif len(candidates) > 1:
            logging.warning('THERE IS ANOTHER MOVE')
            return [candidates[0][COL], candidates[0][ROW], toCOL, toROW, promote]
        else:
            logging.info('THERE IS NO MOVE')
            return False

    # in case the format does not match
    else:
        # check whether it represents castling
        if player == WHITE:
            row = 1 - 1
        elif player == BLACK:
            row = 8 - 1
        else:
            logging.critical('UNEXPECTED PLAYER VALUE in s_analyze')
            return False

        # Q-side
        if s in ['O-O-O', 'o-o-o', '0-0-0'] and board[e - 1][row] == player * KING:
            logging.info('format is {}'.format(s))
            return [e - 1, row, c - 1, row, EMPTY]
        # K-side
        elif s in ['O-O', 'o-o', '0-0'] and board[e - 1][row] == player * KING:
            logging.info('format is {}'.format(s))
            return [e - 1, row, g - 1, row, EMPTY]
        else:
            logging.debug('INVALID FORMAT')
            return False


def instruction():
    print('''
    In order to study chess properly, and also to play in leagues and tournaments, you need to be able to read and write chess moves. There are a few ways to record chess moves, but on this site we will be using standard algebraic notation, which is the notation required by FIDE (the international chess federation).

    -- The board
    In algebraic notation, we use a system of alphanumeric co-ordinates to identify each square. The ranks (horizontal rows) are identified with numbers starting from white's side of the board, and the files (vertical columns) are identified by letters, starting from white's left. On the board below, co-ordinates are displayed for every square.

            a   b   c   d   e   f   g   h
           -------------------------------
        8 | a8| b8| c8| d8| e8| f8| g8| h8| 8
           -------------------------------
        7 | a7| b7| c7| d7| e7| f7| g7| h7| 7
           -------------------------------
        6 | a6| b6| c6| d6| e6| f6| g6| h6| 6
           -------------------------------
        5 | a5| b5| c5| d5| e5| f5| g5| h5| 5
           -------------------------------
        4 | a4| b4| c4| d4| e4| f4| g4| h4| 4
           -------------------------------
        3 | a3| b3| c3| d3| e3| f3| g3| h3| 3
           -------------------------------
        2 | a2| b2| c2| d2| e2| f2| g2| h2| 2
           -------------------------------
        1 | a1| b1| c1| d1| e1| f1| g1| h1| 1
           -------------------------------
            a   b   c   d   e   f   g   h

    The co-ordinates are the same whether you are looking at the board from white's perspective or black's.

    -- Recording a move
    With the exception of the knight, each piece is represented by the first letter of its name, capitalised. Knight starts with the same letter as king, so for the knights we use the letter N instead. When we record a move, we record the piece that is being moved, and the square that the piece is being moved to. For example:

        Bc4 - Bishop moves to the c4 square.
        Nf3 - Knight moves to the f3 square.
        Qc7 - Queen moves to the c7 square.
    
    The only exception to this is pawn moves. When a pawn moves, we don't normally bother to record the P, just the square that the pawn is moving to. For example:

        e4 - pawn moves to the e4 square.
        g6 - pawn moves to the g6 square.
    
    If the pawn has reached the far side of the board and promoted, use an '=' sign to show which piece it was promoted to. For example:

        b8=Q - pawn moves to the b8 square and promotes to a queen.
        h1=N - pawn moves to the h1 square and promotes to a knight.
    
    Simple enough so far. There are also a couple of extra symbols used to indicate certain things about a move. To indicate a capture, we place an 'x' symbol beween the piece and the square, for example:

        Rxf5 - Rook captures a piece on the f5 square.
        Kxd2 - King captures a piece on the d2 square.
    
    When a pawn is capturing, we use the letter of the file it is moving from, then the x, then the square it is moving to. For example:

        gxf6 - Pawn on the g-file captures a piece on the f6 square.
        exd5 - Pawn on the e-file captures a piece on the d5 square.
    
    If the pawn is making an en passant capture, we record the square that the pawn finished on, not the square of the captured pawn. You can also add 'e.p.' after the move to indicate en passant if you want, but this isn't mandatory. For example:

        exd6 - Pawn captures a pawn on d5 en passant. The pawn finishes its move on d6.
        gxh6 e.p. - Pawn captures a pawn on h5 en passant. The pawn finishes its move on h6.
    
    To indicate that a move is check, just add a '+' symbol on the end. If it's a double check, you can add ++ if you like, but just one will do. If the it's a checkmate, use the '#' symbol instead. Here are some examples:

        Ba3+ - Bishop moves to a3 and gives check.
        Qxh7# - Queen captures a piece on h7 and checkmates the black king.
        f3+ - Pawn moves to f3 and gives check.
    
    Sometimes, two different piece of the same type could move to the same square. To specify which piece is to move, add the letter of the file the piece is moving from. Here are some examples:

        Rad1 - Rook on the a-file moves to d1.
        Nbxd2 - Knight on the b-file captures a piece on d2.
        Rfe1+ - Rook on the f-file moves to e1 and gives check.
    
    What about if both pieces are on the same file as well? In this case, put the number of the starting rank for the piece that is moving, instead of the file letter. Here are some examples:

        R7e4 - Rook on the seventh rank moves to e4.
        N1xc3 - Knight on the first rank captures a piece on c3.

    Castling is recorded differently to the other moves. For kingside castling, record it as O-O and for queenside castling, record it as O-O-O.

    When a game has been annotated, some symbols are used to indicate that a particular move is good or bad. We don't normally use these when recording a game in a tournament (it might be offputting to your opponent to see what you think of his moves). The symbols are as follows:

        ! - Good move.
        !! - Brilliant move.
        ? - Poor move.
        ?? - Terrible move.
        !? - Interesting move.
        ?! - Dubious move.


    Did you get it?
    Read the whole passage and press enter to next
    ''')
    input()

