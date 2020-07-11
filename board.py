#! /usr/bin/env python3
# board.py
# programmed by Saito-Saito-Saito
# explained on https://Saito-Saito-Saito.github.io/chess
# last updated: 11/7/2020


import copy
import re
import sys

from config import *
import fundam
import IO


local_logger = setLogger(__name__)



class Board:    
    def __init__(self, *, board=[], target=[OVERSIZE, OVERSIZE], castl_k=[WHITE, BLACK], castl_q=[WHITE, BLACK], player=WHITE, turn=1, s='', logger=local_logger):
        # NOTE: when copying any list, you have to use copy.deepcopy
        if len(board) == SIZE:
            self.board = copy.deepcopy(board)
        else:
            # [0][0] is white's R, [0][1] is white's P, ...
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
        self.ep_target = copy.deepcopy(target) # for en passan
        self.castl_k = copy.deepcopy(castl_k)   # for castling
        self.castl_q = copy.deepcopy(castl_q)   # for castling
        self.turn = turn  # starts from 1
        self.player = player
        self.s = s
        self.logger = logger
                        

    def print(self, *, turnmode=True, reverse=False):
        # cf. boardprint.py
        start = [SIZE - 1, 0]  # WHITESIDE: start[0] BLACKSIDE: start[1]
        stop = [-1, SIZE]  # WHITESIDE: stop[0] BLACKSIDE: stop[1]
        step = [-1, +1] # WHITESIDE: step[0] BLACKSIDE: step[1]
        switch = bool(turnmode and (self.player == BLACK))
        if reverse:
            switch = not switch
            
        print('\n')
        if switch:
            print('\t    h   g   f   e   d   c   b   a')
        else:
            print('\t    a   b   c   d   e   f   g   h')
        print('\t   -------------------------------')
        for rank in range(start[switch], stop[switch], step[switch]):    # down to less
            print('\t{} |'.format(rank + 1), end='')
            for file in range(start[not switch], stop[not switch], step[not switch]):
                print(' {} |'.format(IO.ToggleType(self.board[file][rank])), end='')
            print(' {}'.format(rank + 1))
            print('\t   -------------------------------')
        if switch:
            print('\t    h   g   f   e   d   c   b   a')
        else:
            print('\t    a   b   c   d   e   f   g   h')
        print('\n')
    

    def motionjudge(self, frFILE, frRANK, toFILE, toRANK, promote=EMPTY, logger=None):
        # logger setting
        logger = logger or self.logger
        
        # inside / out of the board
        if not (fundam.InSize(frFILE) and fundam.InSize(frRANK) and fundam.InSize(toFILE) and fundam.InSize(toRANK)):
            logger.debug('OUT OF THE BOARD')
            return False

        player = fundam.PosNeg(self.board[frFILE][frRANK])
        piece = abs(self.board[frFILE][frRANK])
        
        # moving to the square where there is  own piece
        if fundam.PosNeg(self.board[toFILE][toRANK]) == player:
            logger.debug('MOVING TO OWN SQUARE')
            return False

        # there is no piece at Fr
        if piece == EMPTY:
            logger.debug('MOVING EMPTY')
            return False

        # PAWN
        elif piece == PAWN:
            # not promoting at the edge
            if (toRANK == 8 - 1 or toRANK == 1 - 1) and promote not in [R, N, B, Q]:
                logger.info('NECESSARY TO PROMOTE')
                return False
            # normal motion (one step forward); the same FILE, appropriate RANK, TO = EMPTY
            # NOTE: if player is WHITE (=1), the rank number has to increase. vice versa
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
            # all other pawn moves are invalid
            logger.debug('INVALID MOTION of PAWN')
            return False

        # ROOK
        elif piece == ROOK:
            # invalid motion; not moving on the same file/rank
            if frFILE != toFILE and frRANK != toRANK:
                logger.debug('INVALID MOTION of ROOK')
                return False
            # else, necessary to check whether there is an obstacle in the way

        # KNIGHT
        elif piece == KNIGHT:
            # valid motion
            if (abs(toFILE - frFILE) == 1 and abs(toRANK - frRANK) == 2) or (abs(toFILE - frFILE) == 2 and abs(toRANK - frRANK) == 1):
                return True
            # all other motions are invalid
            logger.debug('INVALID MOTION of KNIGHT')
            return False

        # BISHOP
        elif piece == BISHOP:
            # invalid motion; not moving on the same diagonal
            if abs(toFILE - frFILE) != abs(toRANK - frRANK):
                logger.debug('INVALID MOTION of BISHOP')
                return False
            # else, necessary to check an obstacle in the way

        # QUEEN
        elif piece == QUEEN:
            # invalid motion (cf, B/R)
            if frFILE != toFILE and frRANK != toRANK and abs(toFILE - frFILE) != abs(toRANK - frRANK):
                logger.debug('INVALID MOTION of QUEEN')
                return False
            # else, necessary to check an obstacle in the way

        # KING
        elif piece == KING:
            # normal motion (one step)
            if abs(toFILE - frFILE) <= 1 and abs(toRANK - frRANK) <= 1:
                logger.debug('KING NORMAL')
                return True
            # preparing for castling; setting rank
            if player == WHITE:
                rank = 1 - 1
            elif player == BLACK:
                rank = 8 - 1
            else:
                logger.error('UNEXPECTED PLAYER VALUE in motionjudge')
                print('SYSTEM ERROR')
                sys.exit('SYSTEM ERROR')
            # Q-side; adequate fr and to, all passing squares are EMPTY
            if player in self.castl_q and frFILE == e - 1 and frRANK == rank and toFILE == c - 1 and toRANK == rank and self.board[b - 1][rank] == self.board[c - 1][rank] == self.board[d - 1][rank] == EMPTY:
                # K must not be checked while castling
                for ran in range(SIZE):
                    for fil in range(SIZE):
                        if fundam.PosNeg(self.board[fil][ran]) == -player and (self.motionjudge(fil, ran, e - 1, rank, Q) or self.motionjudge(fil, ran, d - 1, rank, Q) or self.motionjudge(fil, ran, c - 1, rank, Q)):
                            logger.info('CHECKED IN THE WAY')
                            return False
                logger.debug('KING Q-side')
                return True
            # K-side; adequate fr and to, all passing squares are EMPTY
            if player in self.castl_k and frFILE == e - 1 and frRANK == rank and toFILE == g - 1 and toRANK == rank and self.board[f - 1][rank] == self.board[g - 1][rank] == EMPTY:
                # K must be checked while castling
                for ran in range(SIZE):
                    for fil in range(SIZE):
                        if fundam.PosNeg(self.board[fil][ran]) == -player and (self.motionjudge(fil, ran, e - 1, rank, Q) or self.motionjudge(fil, ran, d - 1, rank, Q) or self.motionjudge(fil, ran, c - 1, rank, Q)):
                            logger.info('CHECKED IN THE WAY')
                            return False
                logger.debug('KING K-side')
                return True
            # all other King's moves are invalid
            logger.debug('INVALID MOTION of KING')
            return False

        # other piece values are invalid
        else:
            logger.error('UNEXPECTED VALUE of PIECE in motionjudge')
            print('SYSTEM ERROR')
            sys.exit('SYSTEM ERROR')

        # whether there is an obstacle in the wauy of R/B/Q
        direction = [fundam.PosNeg(toFILE - frFILE), fundam.PosNeg(toRANK - frRANK)]
        focused = [frFILE + direction[FILE], frRANK + direction[RANK]]  # focused square
        while focused[FILE] != toFILE or focused[RANK] != toRANK:   # while not reaching TO
            # out of the board
            if not (fundam.InSize(focused[0]) and fundam.InSize(focused[1])):
                logger.warning('')
                break
            # if there is a piece on the way
            if self.board[focused[FILE]][focused[RANK]] != EMPTY:
                logger.debug('THERE IS AN OBSTACLE in the way')
                return False
            # controlling parameters 
            focused[FILE] += direction[FILE]
            focused[RANK] += direction[RANK]
        # there is nothing in the wauy
        return True

    
    def move(self, frFILE, frRANK, toFILE, toRANK, promote=EMPTY, logger=None):
        # logger setup
        logger = logger or self.logger
        
        ### INVALID MOTON
        if self.motionjudge(frFILE, frRANK, toFILE, toRANK, promote) == False:
            return False
        
        ### NOT OWN PIECE
        if fundam.PosNeg(self.board[frFILE][frRANK]) != self.player:
            logger.debug('MOVING OPPONENT PIECE OR EMPTY')
            return False

        piece = abs(self.board[frFILE][frRANK])

        ### SPECIAL EVENTS
        # castling
        if piece == KING and abs(toFILE - frFILE) > 1:
            # preparing the rank
            if self.player == WHITE:
                rank = 1 - 1
            elif self.player == BLACK:
                rank = 8 - 1
            else:
                logger.error('UNEXPECTED VALUE of PLAYER in move')
                print('SYSTEM ERROR')
                sys.exit('SYSTEM ERROR')
            # moving rook
            if toFILE == c - 1:
                self.board[d - 1][rank] = self.player * ROOK
                self.board[a - 1][rank] = EMPTY
            elif toFILE == g - 1:
                self.board[f - 1][rank] = self.player * ROOK
                self.board[h - 1][rank] = EMPTY
            else:
                logger.error('UNEXPECTED VALUE of toFILE in move')
                return False
        # en passant; pawn moves diagonal and TO is EMPTY
        if piece == PAWN and frFILE != toFILE and self.board[toFILE][toRANK] == EMPTY:
            # capturing opponent's pawn
            self.board[self.ep_target[FILE]][self.ep_target[RANK]] = EMPTY        
        # promotion; changing the moving piece into promote
        if piece == PAWN and (toRANK == 8 - 1 or toRANK == 1 - 1):
            self.board[frFILE][frRANK] = self.player * promote
        
        ### MOVING OWN PIECE
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
        
        ### RETURN AS SUCCEEDED
        logger.info('SUCCESSFULLY MOVED')
        return True


    def king_place(self, searcher):
        # searching for the searcher's king
        for fil in range(SIZE):
            if searcher * KING in self.board[fil]:
                return [fil, self.board[fil].index(searcher * KING)]
        else:
            # there is no king
            return EMPTY
            

    def checkcounter(self, checkee, logger=None):
        # logger setup
        logger = logger or self.logger
        
        #if there is no king, impossible to check
        TO = self.king_place(checkee)
        try:
            toFILE = TO[FILE]
            toRANK = TO[RANK]
        except:
            logger.info('THERE IS NO KING ON THE BOARD')
            return False

        # searching all the squares, count up the checking pieces
        count = 0
        for frFILE in range(SIZE):
            for frRANK in range(SIZE):
                # pawn might capture the king by promoting, so do not forget promote=Q or something
                if fundam.PosNeg(self.board[frFILE][frRANK]) == -checkee and self.motionjudge(frFILE, frRANK, toFILE, toRANK, Q):
                    logger.info('CHECK: {}, {} -> {}, {}'.format(frFILE, frRANK, toFILE, toRANK))
                    count += 1
        # if checkee is not checked, return 0
        return count


    def checkmatejudge(self, matee, logger=None):
        # logger setup
        logger = logger or self.logger
        
        # if not checked, it's not checkmate
        if self.checkcounter(matee) in [False, 0]:
            logger.debug('NOT CHECKED')
            return False
        
        # searching all the moves matee can
        for frFILE in range(SIZE):
            for frRANK in range(SIZE):
                if fundam.PosNeg(self.board[frFILE][frRANK]) == matee:
                    # searching all TO the piece can reach
                    for toFILE in range(SIZE):
                        for toRANK in range(SIZE):
                            # cloning board
                            local_board = Board(board=self.board, target=self.ep_target, castl_k=self.castl_k, castl_q=self.castl_q, player=matee)
                            # moving the local board and count up check
                            if local_board.move(frFILE, frRANK, toFILE, toRANK, Q) and local_board.checkcounter(matee) == 0:
                                logger.info('THERE IS {}, {} -> {}, {}'.format(frFILE,frRANK,toFILE,toRANK))
                                return False
                    logger.debug('"FR = {}, {}" was unavailable'.format(frFILE, frRANK))

        # completing the loop, there is no way to flee
        return True

    
    def stalematejudge(self, matee, logger=None):
        # logger setup
        logger = logger or self.logger
        
        # if checked, it's not stalemate
        if self.checkcounter(matee) not in [0, False]:
            logger.debug('CHECKED')
            return False

        # searching all the moves matee can
        for frFILE in range(SIZE):
            for frRANK in range(SIZE):
                if fundam.PosNeg(self.board[frFILE][frRANK]) == matee:
                    # searching all TO the piece can reach
                    for toFILE in range(SIZE):
                        for toRANK in range(SIZE):
                            # cloning board
                            local_board = Board(board=self.board, target=self.ep_target, castl_k=self.castl_k, castl_q=self.castl_q, player=matee)
                            # moving the local board and count up check
                            if local_board.move(frFILE, frRANK, toFILE, toRANK, Q) and local_board.checkcounter(matee) == 0:
                                logger.info('THERE IS {}, {} -> {}, {}'.format(frFILE,frRANK,toFILE,toRANK))
                                return False
                    logger.debug('"FR = {}, {}" was unavailable'.format(frFILE, frRANK))
        # completing the loop, there is no way to avoid check when moving
        logger.info('STALEMATE. {} cannot move'.format(self.player))
        return True
    

    def s_analyze(self, logger=None):
        # logger setup
        logger = logger or self.logger
        
        # removing spaces
        self.s = self.s.replace(' ', '').replace('!', '').replace('?', '')

        # avoiding bugs
        if len(self.s) == 0:
            logger.debug('len(s) == 0')
            return False

        # the pattern of the normal format
        match = re.match(r'^[PRNBQK]?[a-h]?[1-8]?[x]?[a-h][1-8](=[RNBQ]|e.p.)?[\++#]?$', self.s)

        # normal format
        if match:
            line = match.group()
            logger.info('line = {}'.format(line))

            # what piece is moving
            if line[0] in ['P', 'R', 'N', 'B', 'Q', 'K']:
                piece = IO.ToggleType(line[0])
                # deleting the info of piece because we do not use it any more
                line = line.lstrip(line[0]) 
            else:
                piece = PAWN
            logger.info('PIECE == {}'.format(piece))

            # written info of what rank the piece comes from; frRANK starts from 0
            if line[0].isdecimal():
                frFILE = OVERSIZE
                frRANK = IO.ToggleType(line[0]) - 1
                # deleting the number so that the sentence seems simpler
                line = line.lstrip(line[0])
            # written info of what file the piece comes from; frFILE starts from 0
            elif ord('a') <= ord(line[0]) <= ord('h') and ord('a') <= ord(line[1]) <= ord('x'):
                frFILE = IO.ToggleType(line[0]) - 1
                frRANK = OVERSIZE
                # deleting only the first character of line
                line = line[1:]
            # nothing is written about where the piece comes from
            else:
                frFILE = OVERSIZE
                frRANK = OVERSIZE
            logger.info('FR = {}, {}'.format(frFILE, frRANK))

            # whether the piece has captured one of the opponent's pieces
            if line[0] == 'x':
                CAPTURED = True
                line = line.lstrip(line[0])
            else:
                CAPTURED = False

            # where the piece goes to; toFILE and toRANK starts from 0
            toFILE = IO.ToggleType(line[0]) - 1
            toRANK = IO.ToggleType(line[1]) - 1
            logger.info('TO = {}, {}'.format(toFILE, toRANK))

            # promotion
            if '=' in line:
                promote = IO.ToggleType(line[line.index('=') + 1])
            else:
                promote = EMPTY
            logger.info('promote = {}'.format(promote))

            # raising up all the available candidates
            candidates = []
            for fil in range(SIZE):
                # when frFILE is written
                if fundam.InSize(frFILE) and frFILE != fil:
                    continue

                for ran in range(SIZE):
                    # when frRANK is written
                    if fundam.InSize(frRANK) and frRANK != ran:
                        continue

                    # piece
                    if self.board[fil][ran] != self.player * piece:
                        continue

                    # available motion
                    if self.motionjudge(fil, ran, toFILE, toRANK, promote) == False:
                        continue

                    candidates.append([fil, ran])
            logger.info('candidates = {}'.format(candidates))

            # checking all the candidates
            for reference in range(len(candidates)):
                # copying and moving the board
                local_board = Board(board=self.board, target=self.ep_target, castl_k=self.castl_k, castl_q=self.castl_q, player=self.player, turn=self.turn, s=self.s)
                local_board.move(candidates[reference][FILE], candidates[reference][RANK], toFILE, toRANK, promote)

                # capture; searching for the opponent's piece that has disappeared
                if CAPTURED or 'e.p.' in line:
                    # normal capturing
                    if fundam.PosNeg(self.board[toFILE][toRANK]) == -self.player:
                        pass
                    # en passan to Q-side
                    elif fundam.InSize(toRANK - 1) and fundam.PosNeg(self.board[toFILE][toRANK - 1]) == -self.player and fundam.PosNeg(local_board.board[toFILE][toRANK - 1]) == EMPTY:
                        pass
                    # en passan to K-side
                    elif fundam.InSize(toRANK + 1) and fundam.PosNeg(self.board[toFILE][toRANK + 1]) == -self.player and fundam.PosNeg(local_board.board[toFILE][toRANK + 1]) == EMPTY:
                        pass
                    # here no piece can capture a piece
                    else:
                        logger.info('{} does not capture any piece'.format(candidates[reference]))
                        del candidates[reference]
                        reference -= 1  # back to the for loop's head, reference increases
                        continue
                
                # check
                if line.count('+') > local_board.checkcounter(-self.player):
                    logger.info('{} is short of the number of check'.format(candidates[reference]))
                    del candidates[reference]
                    reference -= 1  # back to the for loop's head, reference increases
                    continue

                # checkmate
                if '#' in line and local_board.checkmatejudge(-self.player) == False:
                    logger.info('{} does not checkmate'.format(candidates[reference]))
                    del candidates[reference]
                    reference -= 1  # back to the for loop's head, reference increases
                    continue

                # en passant
                if 'e.p.' in line and self.board[toFILE][toRANK] != EMPTY:
                    logger.info('{} does not en passant'.format(candidates[reference]))
                    del candidates[reference]
                    reference -= 1  # back to the for loop's head, reference increases
                    continue

            # normal return
            if len(candidates) == 1:
                logger.info('NORMALLY RETURNED')
                return [candidates[0][FILE], candidates[0][RANK], toFILE, toRANK, promote]
            # when some candidates are available
            elif len(candidates) > 1:
                logger.warning('THERE IS ANOTHER MOVE')
                return [candidates[0][FILE], candidates[0][RANK], toFILE, toRANK, promote]
            # no candidates are available
            else:
                logger.info('THERE IS NO MOVE')
                return False

        # in case the format does not match
        else:
            # game set; take note that player themselves cannot win by inputting these codes
            if self.s == '1/2-1/2':
                logger.info('DRAW GAME')
                return EMPTY
            elif self.s == '1-0' and self.player == BLACK:
                logger.info('WHITE WINS')
                return WHITE
            elif self.s == '0-1' and self.player == WHITE:
                logger.info('BLACK WINS')
                return BLACK
            
            # check whether it represents castling
            # rank setting
            if self.player == WHITE:
                rank = 1 - 1
            elif self.player == BLACK:
                rank = 8 - 1
            else:
                logger.error('UNEXPECTED PLAYER VALUE in s_analyze')
                print('SYSTEM ERROR')
                sys.exit('SYSTEM ERROR')
            # Q-side
            if self.s in ['O-O-O', 'o-o-o', '0-0-0'] and self.board[e - 1][rank] == self.player * KING:
                logger.info('format is {}, castl is {}'.format(self.s, self.castl_q))
                return [e - 1, rank, c - 1, rank, EMPTY]
            # K-side
            elif self.s in ['O-O', 'o-o', '0-0'] and self.board[e - 1][rank] == self.player * KING:
                logger.info('format is {}, castl is {}'.format(self.s, self.castl_k))
                return [e - 1, rank, g - 1, rank, EMPTY]
            
            # invalid format
            else:
                logger.debug('INVALID FORMAT')
                return False


    def record(self, address, logger=None):
        # logger setup
        logger = logger or self.logger
        
        # removing spaces, !, ?
        self.s = self.s.replace(' ', '').replace('!', '').replace('?', '')

        # avoiding bugs
        if len(self.s) == 0:
            logger.debug('len(s) == 0')
            return False

        # normal pattern
        match = re.match(r'^[PRNBQK]?[a-h]?[1-8]?[x]?[a-h][1-8](=[RNBQ]|e.p.)?[\++#]?$', self.s)
        # normal pattern matched
        if match:
            s_record = match.group()
        # resign
        elif self.s in ['1-0', '0-1', '1/2-1/2']:
            s_record = self.s
        # castling
        elif self.s in ['O-O-O', 'O-O', 'o-o-o', 'o-o', '0-0-0', '0-0']:
            s_record = self.s.replace('o', 'O').replace('0', 'O')
        # invalid format
        else:
            logger.info('OUT OF FORMAT in record')
            return False
        
        # open the recording file
        f = open(address, 'a')

        # WHITE WINS (BLACK DIDN'T MOVE)
        if s_record == '1-0':
            f.write('1-0')
        # BLACK WINS (WHITE DIDN'T MOVE)
        elif s_record == '0-1':
            f.write('{}\t0-1'.format(self.turn))
        # writing on WHITE side
        elif self.player == WHITE:
            f.write('{}\t'.format(self.turn) + s_record.ljust(12))
        # writing on BLACK side
        elif self.player == BLACK:
            f.write(s_record.ljust(12) + '\n')
        else:
            logger.error('UNEXPECTED VALUE of PLAYER in record')
            print('SYSTEM ERROR')
            sys.exit('SYSTEM ERROR')
        
        f.close()

        # return as succeeded
        return True


    def tracefile(self, destination_turn, destination_player, isrecwrite=True, logger=None):
        # logger setup
        logger = logger or self.logger
        
        # back to the first
        if destination_turn == 1 and destination_player == WHITE:
            local_board = Board()
            return local_board

        # preparing (initializing) the sub file; all the local moves are recorded on the sub file
        open(SUBRECADDRESS, 'w').close()
        # reading the main file
        f = open(MAINRECADDRESS, 'r')
        # deleting first and last spaces
        line = f.read()
        line = line.strip()
        f.close()
        logger.info('line is "{}"'.format(line))

        # local Board
        local_board = Board()
        
        # detectong each letter in line
        for letter in line:
            # when you come to the end of a sentence
            if letter in [' ', '\t', '\n', ',', '.']:
                logger.info('local_s is {}'.format(local_board.s))
                motion = local_board.s_analyze()
                # normal motion
                if type(motion) is list:
                    local_board.move(*motion)
                    local_board.record(SUBRECADDRESS)  # all the local moves are recorded on the sub file
                    if local_board.player == BLACK:
                        local_board.turn += 1
                    local_board.player *= -1
                    # destination
                    if local_board.turn == destination_turn and local_board.player == destination_player:
                        logger.info('trace succeeded')
                        if isrecwrite:
                            # copying the file
                            f = open(MAINRECADDRESS, 'w')
                            g = open(SUBRECADDRESS, 'r')
                            f.write(g.read())
                            f.close()
                            g.close()
                        return local_board
                # game set
                elif type(motion) is int:
                    print('GAME SET')
                    if isrecwrite:
                        # copying the record
                        f = open(MAINRECADDRESS, 'w')
                        g = open(SUBRECADDRESS, 'r')
                        f.write(g.read())
                        f.close()
                        g.close()
                    return motion
                # initializing the local_s
                local_board.s = ''
            # the sentence does not end yet
            else:
                local_board.s = ''.join([local_board.s, letter])
                logger.debug('local_s = {}'.format(local_board.s))

        # last one local_s; the same as in the for loop
        logger.info('local_s is {}'.format(local_board.s))
        motion = local_board.s_analyze()
        if type(motion) is list:
            local_board.move(*motion)
            local_board.record(SUBRECADDRESS)
            if local_board.player == BLACK:
                local_board.turn += 1
            local_board.player *= -1
            # reaching destination
            if local_board.turn == destination_turn and local_board.player == destination_player:
                logger.info('trace succeeded')
                if isrecwrite:
                    f = open(MAINRECADDRESS, 'w')
                    g = open(SUBRECADDRESS, 'r')
                    f.write(g.read())
                    f.close()
                    g.close()
                return local_board
        elif type(motion) is int:
            if isrecwrite:
                f = open(MAINRECADDRESS, 'w')
                g = open(SUBRECADDRESS, 'r')
                f.write(g.read())
                f.close()
                g.close()
            return motion

        # reaching here, you cannot trace
        logger.warning('FAILED TO BACK')
        return self


if __name__ == "__main__":
    local_board = Board()
    local_board.print()
    local_board.move(c - 1, 2 - 1, c - 1, 4 - 1)
    local_board.player *= -1
    local_board.print(turnmode=True)
    local_board.move(c - 1, 7 - 1, c - 1, 6 - 1)
    local_board.player *= -1
    local_board.print(turnmode=True)
    print(local_board.king_place(WHITE))
    print(local_board.king_place(BLACK))