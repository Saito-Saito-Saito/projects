#! usr/bin/env python3
# __main__.py


from config import *
import IO
import csjudge
import move


player = WHITE
ep_target = [OVERSIZE, OVERSIZE]
castl_k = [WHITE, BLACK]
castl_q = [WHITE, BLACK]

IO.BoardPrint()


while True:
    ### game set judge
    # KING captured
    for col in range(SIZE):
        if K * player in main_board[col]:
            break
    else:
        logging.info('KING has been captured')
        winner = -player
        break
    # checckmate
    if csjudge.checkmatejudge(player):
        winner = -player
        break
    # stalemate
    if csjudge.stalematejudge(player):
        winner = EMPTY
        break

    ### input
    if player == WHITE:
        print('WHITE (X to give up / H to show help) >>> ', end='')
    elif player == BLACK:
        print('BLACK (X to give up / H to show help) >>> ', end='')
    else:
        logging.critical('UNEXPECTED PLAYER VALUE in while')
        print('SYSTEM ERROR')
        winner = EMPTY
        break
    s = input()

    # deleting all the spaces in s
    s = s.replace(' ', '')

    # giving up
    if s == 'X' or s == 'x' or (player == WHITE and s == '0-1') or (player == BLACK and s == '1-0'):
        winner = -player
        break
    # draw
    elif s == '1/2-1/2':
        if player == WHITE:
            print('Do you agree, BLACK (y/n)? >>> ', end='')
        elif player == BLACK:
            print('Do you agree, WHITE (y/n)? >>> ', end='')
        else:
            logging.critical('UNEXPECTED PLAYER VALUE in while')
            winner = EMPTY
            break
        ch = input()
        if ch == 'y' or ch == 'Y':
            winner = EMPTY
            break
        else:
            continue
    # help
    elif s == 'h' or s == 'H':
        IO.instruction()
        continue

    # analyzing the formatted s
    motion = IO.s_analyze(s, player)
    logging.warning('motion = {}'.format(motion))
    if motion == False:
        print('INVALID INPUT/MOTION')
        continue

    move.move(motion[0], motion[1], motion[2], motion[3], motion[4])

    ### parameter control
    piece = abs(main_board[motion[2]][motion[3]])
    # ep_target for e.p.
    if piece == PAWN and abs(motion[3] - motion[1]) == 2:
        ep_target = [motion[2], motion[3]]
    else:
        ep_target = [OVERSIZE, OVERSIZE]
    logging.info('ep_target = {}'.format(ep_target))
    # castl_q
    if player in castl_q and (piece == KING or (piece == ROOK and motion[0] == a - 1)):
        castl_q.remove(player)
    logging.info('castl_q = {}'.format(castl_q))
    # castl_k
    if player in castl_k and (piece == KING or (piece == ROOK and motion[0] == h - 1)):
        castl_k.remove(player)
    logging.info('castl_k = {}'.format(castl_k))
    # player
    player *= -1

    IO.BoardPrint()


print('GAME SET')
if winner == EMPTY:
    print('1/2 - 1/2\tDRAW')
elif winner == WHITE:
    print('1 - 0\tWHITE WINS')
elif winner == BLACK:
    print('0 - 1\tBLACK WINS')
else:
    print('SYSTEM ERROR')
    logging.critical('UNEXPECTED WINNER VALUE out of the while')
print('\n')

