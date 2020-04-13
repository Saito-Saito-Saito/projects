#! /usr/bin/env python3
# board.py

import re
import copy
import sys

from config import *
import fundam
import IO


class Board:    
    def __init__(self, input_board=[], input_taget=[OVERSIZE, OVERSIZE], input_k=[WHITE, BLACK], input_q=[WHITE, BLACK], input_player=WHITE):
        if len(input_board) == 8:
            self.board = copy.deepcopy(input_board)
        else:
            self.board = [
                [R, P, 0, 0, 0, 0, -P, -R],
                [N, P, 0, 0, 0, 0, -P, -N],
                [B, P, 0, 0, 0, 0, -P, -B],
                [Q, P, 0, 0, 0, 0, -P, -Q],
                [K, P, 0, 0, 0, 0, -P, -K],
                [B, P, 0, 0, 0, 0, -P, -B],
                [N, P, 0, 0, 0, 0, -P, -N],
                [R, P, 0, 0, 0, 0, -P, -R]
            ]
        self.ep_target = input_taget
        self.castl_k = input_k
        self.castl_q = input_q
        self.turn = 1
        self.player = input_player
        self.s = ''
                        

    def BOARDprint(self):
        print('\n')
        print('\t    a   b   c   d   e   f   g   h')
        print('\t   -------------------------------')
        for rank in range(SIZE - 1, -1, -1):
            print('\t{} |'.format(rank + 1), end='')
            for file in range(SIZE):
                print(' {} |'.format(IO.ToggleType(self.board[file][rank])), end='')
            print(' {}'.format(rank + 1))
            print('\t   -------------------------------')
        print('\t    a   b   c   d   e   f   g   h')
        print('\n')
    

    def motionjudge(self, frFILE, frRANK, toFILE, toRANK, promote=EMPTY):
        # inside / out of the board
        if not (fundam.InSize(frFILE) and fundam.InSize(frRANK) and fundam.InSize(toFILE) and fundam.InSize(toRANK)):
            logging.debug('OUT OF THE BOARD')
            return False

        player = fundam.PosNeg(self.board[frFILE][frRANK])
        piece = abs(self.board[frFILE][frRANK])
        
        # moving to the square where there is  own piece
        if fundam.PosNeg(self.board[toFILE][toRANK]) == player:
            logging.debug('MOVING TO OWN SQUARE')
            return False

        # there is no piece at Fr
        if piece == EMPTY:
            logging.debug('MOVING EMPTY')
            return False

        # PAWN
        elif piece == PAWN:
            # not promoting at the edge
            if (toRANK == 8 - 1 or toRANK == 1 - 1) and promote not in [R, N, B, Q]:
                logging.info('NECESSARY TO PROMOTE')
                return False
            # normal motion (one step forward); the same FILE, appropriate RANK, TO = EMPTY
            # note: if player is WHITE (=1), the rank number has to increase
            if frFILE == toFILE and toRANK - frRANK == player and self.board[toFILE][toRANK] == EMPTY:
                return True
            # normal capturing; next FILE, appropriate RANK, TO = opponent
            if abs(toFILE - frFILE) == 1 and toRANK - frRANK == player and fundam.PosNeg(self.board[toFILE][toRANK]) == -player:
                return True
            # first two steps; adequate frRANK the same FILE, appropriate RANK, passing squares are EMPTY
            if ((player == WHITE and frRANK == 2 - 1) or (player == BLACK and frRANK == 7 - 1)) and frFILE == toFILE and toRANK - frRANK == 2 * player and self.board[frFILE][frRANK + player] == self.board[toFILE][toRANK] == EMPTY:
                return True
            # en passant; FR - ep_target, TO - ep_target, TO = EMPTY
            if abs(self.ep_target[FILE] - frFILE) == 1 and frRANK == self.ep_target[RANK] and toFILE == self.ep_target[FILE] and toRANK - self.ep_target[RANK] == player and self.board[toFILE][toRANK] == EMPTY:
                return True
            # all other moves are invalid
            logging.debug('INVALID MOTION of PAWN')
            return False

        # ROOK
        elif piece == ROOK:
            # invalid motion
            if frFILE != toFILE and frRANK != toRANK:
                logging.debug('INVALID MOTION of ROOK')
                return False
            # else, necessary to check whether there is an obstacle in the way

        # KNIGHT
        elif piece == KNIGHT:
            # valid motion
            if (abs(toFILE - frFILE) == 1 and abs(toRANK - frRANK) == 2) or (abs(toFILE - frFILE) == 2 and abs(toRANK - frRANK) == 1):
                return True
            # all other motion is invalid
            logging.debug('INVALID MOTION of KNIGHT')
            return False

        # BISHOP
        elif piece == BISHOP:
            # invalid motion
            if abs(toFILE - frFILE) != abs(toRANK - frRANK):
                logging.debug('INVALID MOTION of BISHOP')
                return False
            # else, necessary to check an obstacle in the way

        # QUEEN
        elif piece == QUEEN:
            # invalid motion (cf, B/R)
            if frFILE != toFILE and frRANK != toRANK and abs(toFILE - frFILE) != abs(toRANK - frRANK):
                logging.debug('INVALID MOTION of QUEEN')
                return False
            # else, necessary to check an obstacle in the way

        # KING
        elif piece == KING:
            # normal motion (one step)
            if abs(toFILE - frFILE) <= 1 and abs(toRANK - frRANK) <= 1:
                logging.info('KING NORMAL')
                return True
            # castling
            if player == WHITE:
                rank = 1 - 1
            elif player == BLACK:
                rank = 8 - 1
            else:
                logging.error('UNEXPECTED PLAYER VALUE in motionjudge')
                print('SYSTEM ERROR')
                sys.exit()
            # Q-side
            if player in self.castl_q and frFILE == e - 1 and frRANK == rank and toFILE == c - 1 and toRANK == rank and self.board[b - 1][rank] == self.board[c - 1][rank] == self.board[d - 1][rank] == EMPTY:
                logging.debug('KING Q-side')
                return True
            # K-side
            if player in self.castl_k and frFILE == e - 1 and frRANK == rank and toFILE == g - 1 and toRANK == rank and self.board[f - 1][rank] == self.board[g - 1][rank] == EMPTY:
                logging.debug('KING K-side')
                return True
            # all other moves are invalid
            logging.debug('INVALID MOTION of KING')
            return False

        # other piece values
        else:
            logging.error('UNEXPECTED VALUE of PIECE in motionjudge')
            print('SYSTEM ERROR')
            sys.exit()

        # whether there is an obstacle in the wauy of R/B/Q
        direction = [fundam.PosNeg(toFILE - frFILE), fundam.PosNeg(toRANK - frRANK)]
        focused = [frFILE + direction[FILE], frRANK + direction[RANK]]
        while focused[FILE] != toFILE or focused[RANK] != toRANK:
            if not (fundam.InSize(focused[0]) and fundam.InSize(focused[1])):
                break
            if self.board[focused[FILE]][focused[RANK]] != EMPTY:
                logging.debug('THERE IS AN OBSTACLE in the way')
                return False
            focused[FILE] += direction[FILE]
            focused[RANK] += direction[RANK]
        # there is nothing in the wauy
        return True

    
    def move(self, frFILE, frRANK, toFILE, toRANK, promote=EMPTY):
        ### INVALID MOTON
        if self.motionjudge(frFILE, frRANK, toFILE, toRANK, promote) == False:
            return False
        
        piece = abs(self.board[frFILE][frRANK])

        ### SPECIAL EVENTS
        # castling
        if piece == KING and abs(toFILE - frFILE) > 1:
            if self.player == WHITE:
                rank = 1 - 1
            elif self.player == BLACK:
                rank = 8 - 1
            else:
                logging.error('UNEXPECTED VALUE of PLAYER in move')
                print('SYSTEM ERROR')
                sys.exit()
            # moving rook
            if toFILE == c - 1:
                self.board[d - 1][rank] = self.player * ROOK
                self.board[a - 1][rank] = EMPTY
            elif toFILE == g - 1:
                self.board[f - 1][rank] = self.player * ROOK
                self.board[h - 1][rank] = EMPTY
            else:
                logging.error('UNEXPECTED VALUE of toFILE in move')
                return False
        # en passant
        if piece == PAWN and frFILE != toFILE and self.board[toFILE][toRANK] == EMPTY:
            # capturing opponent's pawn
            self.board[toFILE][frRANK] = EMPTY        
        # promotion
        if piece == PAWN and (toRANK == 8 - 1 or toRANK == 1 - 1):
            self.board[frFILE][frRANK] = self.player * promote
        # moving own piece
        self.board[toFILE][toRANK] = self.board[frFILE][frRANK]
        self.board[frFILE][frRANK] = EMPTY
        
        ### PARAMETERS CONTROL
        # for e.p.
        if piece == PAWN and abs(toRANK - frRANK) > 1:
            self.ep_target = [toFILE, toRANK]
        else:
            self.ep_target = [OVERSIZE, OVERSIZE]
        # for castling q-side
        if self.player in self.castl_q and (piece == KING or (piece == ROOK and frFILE == a - 1)):
            self.castl_q.remove(self.player)
        # for castling k-side
        if self.player in self.castl_k and (piece == KING or (piece == ROOK and frFILE == h - 1)):
            self.castl_k.remove(self.player)
        # turn count
        if self.player == BLACK:
            self.turn += 1
        # player change
        self.player *= -1
        
        ### RETURN AS SUCCEEDED
        return True


    def king_place(self, searcher):
        # searching for the checkee's king
        for file in range(SIZE):
            if searcher * KING in self.board[file]:
                return [file, self.board[file].index(searcher * KING)]
        else:
            # there is no king
            return EMPTY
            

    def checkcounter(self, checkee):
        #if there is no king, impossible to check
        TO = self.king_place(checkee)
        try:
            toFILE = TO[FILE]
            toRANK = TO[RANK]
        except:
            logging.debug('THERE IS NO KING')
            return False

        # count up the checking pieces
        count = 0
        for frFILE in range(SIZE):
            for frRANK in range(SIZE):
                if fundam.PosNeg(self.board[frFILE][frRANK]) == -checkee and self.motionjudge(frFILE, frRANK, toFILE, toRANK, Q):
                    logging.warning('CHECK: {}, {} -> {}, {}'.format(frFILE, frRANK, toFILE, toRANK))
                    count += 1
        # if checkee is not checked, return 0
        return count


    def checkmatejudge(self, matee):
        # if not checked, it's not checkmate
        if self.checkcounter(matee) in [False, 0]:
            return False
        
        # searching for all the moves matee can
        for frFILE in range(SIZE):
            for frRANK in range(SIZE):
                if fundam.PosNeg(self.board[frFILE][frRANK]) == matee:
                    for toFILE in range(SIZE):
                        for toRANK in range(SIZE):
                            # cloning board
                            local_board = Board(self.board, self.ep_target, self.castl_k, self.castl_q, self.player)
                            if local_board.move(frFILE, frRANK, toFILE, toRANK, Q) and local_board.checkcounter(matee) == 0:
                                logging.info('THERE IS {}, {} -> {}, {}'.format(frFILE,frRANK,toFILE,toRANK))
                                return False
                    logging.info('"FR = {}, {}" was unavailable'.format(frFILE, frRANK))

        # completing the loop, there is no way to flee
        return True

    
    def stalematejudge(self, matee):
        # if checked, it's not stalemate
        if self.checkcounter(matee) not in [0, False]:
            logging.debug('CHECKED')
            return False

        # searching all the moves for one that can move without being checked
        for frFILE in range(SIZE):
            for frRANK in range(SIZE):
                if fundam.PosNeg(self.board[frFILE][frRANK]) == matee:
                    for toFILE in range(SIZE):
                        for toRANK in range(SIZE):
                            local_board = Board(self.board, self.ep_target, self.castl_k, self.castl_q)
                            # in case it is not checked after moving
                            motion = local_board.move(frFILE, frRANK, toFILE, toRANK, Q)
                            count = local_board.checkcounter(matee)
                            logging.debug('motion: {}, count: {}'.format(motion, count))
                            if motion and count in [0, False]:
                                logging.info('THERE IS {}, {} -> {}, {}'.format(frFILE, frRANK, toFILE, toRANK))
                                return False
        # completing the loop, there is no way to avoid check when moving
        return True
    

    def s_analyze(self):
        # avoiding bugs
        if len(self.s) == 0:
            logging.debug('len(s) == 0')
            return False

        # deleting all of !? at the tail
        while self.s[-1] in ['!', '?']:
            self.s = self.s.rstrip(self.s[-1])
            if len(self.s) == 0:
                return False

        # deleting all of SPACE
        self.s = self.s.replace(' ', '')

        # avoiding bugs
        if len(self.s) == 0:
            logging.debug('len(s) == 0')
            return False

        # matching the normal format
        match = re.match(r'^[PRNBQK]?[a-h]?[1-8]?[x]?[a-h][1-8](=[RNBQ]|e.p.)?[\+#]?$', self.s)

        if match:
            line = match.group()
            logging.info('line = {}'.format(line))

            # what piece is moving
            if line[0] in ['R', 'N', 'B', 'Q', 'K']:
                piece = IO.ToggleType(line[0])
                line = line.lstrip(line[0])
            else:
                piece = PAWN
            logging.info('PIECE == {}'.format(piece))

            # written info of what rank the piece comes from
            if line[0].isdecimal():
                frFILE = OVERSIZE
                frRANK = IO.ToggleType(line[0]) - 1
                line = line.lstrip(line[0])
            # written info of what file the piecce comes from
            elif ord('a') <= ord(line[0]) <= ord('h') and ord('a') <= ord(line[1]) <= ord('x'):
                frFILE = IO.ToggleType(line[0]) - 1
                frRANK = OVERSIZE
                line = line.lstrip(line[0])
            # nothing is written about where the piece comes from
            else:
                frFILE = OVERSIZE
                frRANK = OVERSIZE
            logging.info('FR = {}, {}'.format(frFILE, frRANK))

            # whether the piece has captured one of the opponent's pieces
            if line[0] == 'x':
                CAPTURED = True
                line = line.lstrip(line[0])
            else:
                CAPTURED = False

            # where the piece goes to
            toFILE = IO.ToggleType(line[0]) - 1
            toRANK = IO.ToggleType(line[1]) - 1
            logging.info('TO = {}, {}'.format(toFILE, toRANK))

            # promotion
            if '=' in line:
                promote = IO.ToggleType(line[line.index('=') + 1])
            else:
                promote = EMPTY
            logging.info('promote = {}'.format(promote))

            # raising up all the available candidates
            candidates = []
            for file in range(SIZE):
                # when frFILE is written
                if fundam.InSize(frFILE) and frFILE != file:
                    continue

                for rank in range(SIZE):
                    # when frRANK is written
                    if fundam.InSize(frRANK) and frRANK != rank:
                        continue

                    # piece
                    if self.board[file][rank] != self.player * piece:
                        continue

                    # available motion
                    if self.motionjudge(file, rank, toFILE, toRANK, promote) == False:
                        continue

                    candidates.append([file, rank])
            logging.info('candidates = {}'.format(candidates))

            # checking all the candidates
            for reference in range(len(candidates)):
                local_board = Board(self.board, self.ep_target, self.castl_k, self.castl_q, self.player)
                local_board.move(candidates[reference][FILE], candidates[reference][RANK], toFILE, toRANK, promote)

                # capture; searching for the opponent's piece that has disappeared
                if CAPTURED or 'e.p.' in line:
                    if fundam.PosNeg(self.board[toFILE][toRANK]) == -self.player:
                        break
                    if fundam.InSize(toRANK - 1) and fundam.PosNeg(self.board[toFILE][toRANK - 1]) == -self.player and fundam.PosNeg(local_board.board[toFILE][toRANK - 1]) == EMPTY:
                        break
                    if fundam.InSize(toRANK + 1) and fundam.PosNeg(self.board[toFILE][toRANK + 1]) == -self.player and fundam.PosNeg(local_board.board[toFILE][toRANK + 1]) == EMPTY:
                        break
                    # here no piece can capture a piece
                    logging.info('{} does not capture any piece'.format(candidates[reference]))
                    del candidates[reference]
                    reference -= 1
                    continue
                # check
                if line.count('+') > local_board.checkcounter(-self.player):
                    logging.info('{} is short of the number of check'.format(candidates[reference]))
                    del candidates[reference]
                    reference -= 1
                    continue

                # checkmate
                if '#' in line and local_board.checkmatejudge(-self.player) == False:
                    logging.info('{} does not checkmate'.format(candidates[reference]))
                    del candidates[reference]
                    reference -= 1
                    continue

                # en passant
                if 'e.p.' in line and self.board[toFILE][toRANK] != EMPTY:
                    logging.info('{} does not en passant'.format(candidates[reference]))
                    del candidates[reference]
                    reference -= 1
                    continue

            # return
            if len(candidates) == 1:
                logging.info('NORMALLY RETURNED from s_analyze')
                return [candidates[0][FILE], candidates[0][RANK], toFILE, toRANK, promote]
            elif len(candidates) > 1:
                logging.warning('THERE IS ANOTHER MOVE')
                return [candidates[0][FILE], candidates[0][RANK], toFILE, toRANK, promote]
            else:
                logging.info('THERE IS NO MOVE')
                return False

        # in case the format does not match
        else:
            # check whether it represents castling
            if self.player == WHITE:
                rank = 1 - 1
            elif self.player == BLACK:
                rank = 8 - 1
            else:
                logging.error('UNEXPECTED PLAYER VALUE in s_analyze')
                print('SYSTEM ERROR')
                sys.exit()

            # game set
            if self.s == '1/2-1/2':
                logging.info('DRAW GAME')
                return EMPTY
            elif self.s == '1-0' and self.player == BLACK:
                logging.info('WHITE WINS')
                return WHITE
            elif self.s == '0-1' and self.player == WHITE:
                logging.info('BLACK WINS')
                return BLACK
            # Q-side
            elif self.s in ['O-O-O', 'o-o-o', '0-0-0'] and self.board[e - 1][rank] == self.player * KING:
                logging.info('format is {}, castl is {}'.format(self.s, self.castl_q))
                return [e - 1, rank, c - 1, rank, EMPTY]
            # K-side
            elif self.s in ['O-O', 'o-o', '0-0'] and self.board[e - 1][rank] == self.player * KING:
                logging.info('format is {}, castl is {}'.format(self.s, self.castl_k))
                return [e - 1, rank, g - 1, rank, EMPTY]
            else:
                logging.debug('INVALID FORMAT')
                return False


    def record(self, address):
        # avoding bugs
        if len(self.s) == 0:
            logging.debug('len(s) in record is 0')
            return False

        # deleting !? at the end
        while self.s[-1] in ['!', '?']:
            del self.s[-1]
            if len(self.s) == 0:
                logging.debug('len(s) in record is 0')
                return False

        # deleting all spaces
        self.s = self.s.replace(' ', '')

        # avoiding bugs
        if len(self.s) == 0:
            logging.debug('len(s) in record is 0')
            return False

        # normal
        match = re.match(r'^[PRNBQK]?[a-h]?[1-8]?[x]?[a-h][1-8](=[RNBQ]|e.p.)?[\+#]?$', self.s)
        if match:
            s_record = match.group()
        # give up
        elif self.s in ['1-0', '0-1', '1/2-1/2']:
            s_record = self.s
        # castling
        elif self.s in ['O-O-O', 'O-O']:
            s_record = self.s.replace('o', 'O').replace('0', 'O')
        else:
            logging.info('OUT OF FORMAT in record')
            return False
        
        # recording on the file
        f = open(address, 'a')

        # WHITE WINS (BLACK DIDN'T MOVE)
        if s_record == '1-0':
            f.write('1-0')
        # BLACK WINS (WHITE DIDN'T MOVE)
        elif s_record == '0-1':
            f.write('{}\t0-1'.format(self.turn))
        # NOTE: after Board.move, parameter player is changed
        elif -self.player == WHITE:
            f.write('{}\t'.format(self.turn) + s_record.ljust(12))
        elif -self.player == BLACK:
            f.write(s_record.ljust(12) + '\n')
        else:
            logging.error('UNEXPECTED VALUE of PLAYER in record')
            print('SYSTEM ERROR')
            sys.exit()
        
        f.close()

        return True


    def tracefile(self, destination_turn, destination_player, isrecwrite=True):
        # back to the first
        if destination_turn == 1 and destination_player == WHITE:
            local_board = Board()
            return local_board

        # preparing (initializing) the sub file
        open(SUBRECADDRESS, 'w').close()
        # reading the file
        f = open(MAINRECADDRESS, 'r')
        # deleting first and last spaces
        line = f.read().strip(' ').strip('\n')
        f.close()
        logging.info('line is {}'.format(line))

        # valid s holder
        holder = ''
        # local Board
        local_board = Board()
        
        for letter in line:
            if letter in [' ', '\t', '\n']:
                logging.warning('holder is {}'.format(holder))
                local_board.s = holder
                motion = local_board.s_analyze()
                # normal motion
                if type(motion) is list:
                    local_board.move(*motion)
                    local_board.record(SUBRECADDRESS)
                    # destination
                    if local_board.turn == destination_turn and local_board.player == destination_player:
                        logging.info('trace succeeded')
                        # copying the file
                        if isrecwrite:
                            f = open(MAINRECADDRESS, 'w')
                            g = open(SUBRECADDRESS, 'r')
                            f.write(g.read())
                            f.close()
                            g.close()
                        return local_board
                # game set
                elif type(motion) is int:
                    print('GAME SET')
                    # copying the record
                    if isrecwrite:
                        f = open(MAINRECADDRESS, 'w')
                        g = open(SUBRECADDRESS, 'r')
                        f.write(g.read())
                        f.close()
                        g.close()
                    return motion
                holder = ''
            else:
                holder = ''.join([holder, letter])
                logging.info('holder = {}'.format(holder))
                
        # last one holder
        logging.warning('holder is {}'.format(holder))
        local_board.s = holder
        motion = local_board.s_analyze()
        if type(motion) is list:
            local_board.move(*motion)
            local_board.record(SUBRECADDRESS)
            if local_board.turn == destination_turn and local_board.player == destination_player:
                logging.info('trace succeeded')
                # copying the file
                if isrecwrite:
                    f = open(MAINRECADDRESS, 'w')
                    g = open(SUBRECADDRESS, 'r')
                    f.write(g.read())
                    f.close()
                    g.close()
                return local_board
        elif type(motion) is int:
            # copying the record
            if isrecwrite:
                f = open(MAINRECADDRESS, 'w')
                g = open(SUBRECADDRESS, 'r')
                f.write(g.read())
                f.close()
                g.close()
            return motion

        # reaching here, you cannot back
        logging.warning('FAILED TO BACK')
        return self

