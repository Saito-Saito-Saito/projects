#! /usr/bin/env python3
# IO.py
# programmed by Saito-Saito-Saito
# explained on https://Saito-Saito-Saito.github.io/chess
# last updated: 04 March 2021


from config import *

local_logger = setLogger(__name__)


def ToggleType(target, logger=local_logger):
    # piece ID -> piece letter
    if type(target) is int:
        if target == EMPTY:
            return ' '
        elif target == P * BLACK:
            return '♙'
        elif target == R * BLACK:
            return '♖'
        elif target == N * BLACK:
            return '♘'
        elif target == B * BLACK:
            return '♗'
        elif target == Q * BLACK:
            return '♕'
        elif target == K * BLACK:
            return '♔'
        elif target == P * WHITE:
            return '♟'
        elif target == R * WHITE:
            return '♜'
        elif target == N * WHITE:
            return '♞'
        elif target == B * WHITE:
            return '♝'
        elif target == Q * WHITE:
            return '♛'
        elif target == K * WHITE:
            return '♚'
        # invalid target value
        else:
            logger.error('UNEXPECTED INPUT VALUE of A PIECE into IO.ToggleType')
            return False

    # str -> int
    elif type(target) is str:
        # a str number -> int
        if target.isdecimal():
            return int(target)
        # file id
        elif ord('a') &lt;= ord(target) &lt;= ord('h'):
            return ord(target) - ord('a') + 1
        # the kind of piece -> piece no.
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
        # invalid character
        else:
            logger.error('UNEXPECTED INPUT into IO.ToggleType')
            return False

    # unexpected type
    else:
        logger.error('UNEXPECTED INPUT TYPE into IO.ToggleType')
        return False


# for help in the playmode
def instruction():
    print('''
    棋譜の書き方には何通りかありますが、ここでは FIDE (The International Chess Federalation) 公認の standard algebraic notation と呼ばれる記法を使用します。
                
-- 盤面
盤上のマスを一つに絞るのに、数学でやるような「座標」を活用します。横長の行 (rank) は白番から見て下から順に 1, 2, ..., 8 と数え、縦長の列 (file) は白番から見て左から順に a, b, ..., h と番号を振ります。
                
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
                
黒番からみる場合にはこれが 180º 開店した形になります。


-- 駒の動き
各駒の名前は表のように割り振っていきます。

    P - ポーン
    R - ルーク
    N - ナイト
    B - ビショップ
    Q - クイーン
    K - キング

まず駒の名前を書いて、その後にどのマスへ移動したかを記録します。

例）
    Bc4 - ビショップが c4 のマスに動いた
    Nf3 - ナイトが f3 のマスに動いた
    Qc7 - クイーンが c7 のマスに動いた

ポーンはしょっちゅう動かすので、棋譜を書くときは基本的に省略します。

例）
    e4 - ポーンが e4 のマスに動いた
    g6 - ポーンが g6 のマスに動いた
    
ポーンが盤面の端まできてプロモーションしたときは、マスを表す2文字に続けて = (成り上がった後の駒の名前) の形で表します。

例）
    b8=Q - ポーンが b8 にきてクイーンにプロモーションした
    h1=N - ポーンが h1 にきてナイトにプロモーションした

相手の駒を取ったときは x を駒の名前と行き先のマスの間に入れて駒を取ったことを明示します。

例）
    Rxf5 - ルークが相手の駒をとって f5 のマスに移動した
    Kxd2 - キングが相手の駒をとって d2 のマスに移動した

ポーンが相手の駒を取ったときは、ポーンが元々いた列 (file) を表すアルファベットを先頭につけ、続けて x を、さらに移動先のマスを並べます。

例）
    gxf6 - g 列のポーンが相手の駒を取って f6 のマスに移動した
    exd5 - e 列のポーンが相手の駒を取って d5 のマスに移動した

ポーンがアンパッサンして相手の駒を取った場合、駒を取ったポーンの移動先を記録します。アンパッサンしたことを明示するために 'e.p.' をつけたりもしますが、必ずつけなければいけないものではありません。

例）
    exd6 - ポーンがアンパッサンして d5 にある相手のポーンをとり d6 のマスへ移動した
    gxh6 e.p. - ポーンがアンパッサンして h5 にある相手のポーンをとり h6 のマスへ移動した
    
駒を動かして相手にチェックをかけたときは、後ろに + をつけます。ダブルチェックの場合は ++ とする流儀もありますが、1つでも十分です。チェックメイトのときは後ろに # をつけます。

例）
    Ba3+ - ビショップが a3 のマスに移動してチェックとなった
    Qxh7# - クイーンが相手の駒を取って h7 のマスに移動しチェックメイトとなった
    f3+ - ポーンが f3 のマスに移動してチェックとなった
    
これまでご紹介した書き方だけだと、駒の動きを一つに絞れないことがあります。そんなときはどのマスにあった駒を動かしたか明示するために、移動先のマスの前に移動元の列 (file) を表すアルファベットを加えてあげます。

例）
    Rad1 - 元々 a 列にいたルークが d1 のマスに移動した
    Nbxd2 - 元々 b 列にいたナイトが相手の駒を取って d2 のマスに移動した
    Rfe1+ - 元々 f 列にいたルークが e1 のマスに移動してチェックとなった

元々同じ列にいた場合は、元いた行 (rank) を表す数字を先ほどと同じ位置に明示してあげます。

例）
    R7e4 - 元々 7 行にいたルークが e4 のマスに移動した
    N1xc3 - 元々 1 行にいたナイトが相手の駒を取って c3 のマスに移動した

キャスリングはここまであげた場合とは全く異なる書き方で記録します。クイーンサイドにキャスリングしたときは O-O と、キングサイドにキャスリングしたときは O-O-O と記録します。

記録者が感じたことをメモするときに下のような記号を使うこともあります。

    ! - 妙手
    !! - 非常に妙手
    ? - 疑問な手
    ?? - ひどい手
    !? - 面白い手
    ?! - 疑わしい手
    
参照：www.chessstrategyonline.comcontent/tutorials/basic-chess-concepts-chess-notation

    Did you get it?
    Read the whole passage and press enter to next
    ''')
    input()


if __name__=="__main__":
    try:
        print(ToggleType(input('enter a toffled str: ')))
    except:
        print('INVALID INPUT')
    try:
        print(ToggleType(int(input('Enter a toggled int: '))))
    except:
        print('INVALID INPUT')
    input('ENTER TO INSTRUCT')
    instruction()