from itertools import count
from posixpath import split
import numpy as np
import sys

from numpy import ndenumerate, outer
from sklearn import exceptions


# KEY正向左 負向右 (解密) A65 90 a97 122


def Caesar(ciphertxt, key):
    output = ""
    try:
        key = int(key) % 26
    except Exception as e:
        raise SystemExit(
            f"Caesar key is invalid: {key} ") from e
    for w in ciphertxt:
        if (w >= 'A' and w <= 'Z'):
            tmp = (ord(w)-key)
            if tmp > 90:
                tmp = tmp - 26
            elif tmp < 65:
                tmp = tmp + 26
            output = output + chr(tmp)
        elif (w >= 'a' and w <= 'z'):
            tmp = (ord(w)-key)
            if tmp > 122:
                tmp = tmp - 26
            elif tmp < 97:
                tmp = tmp + 26
            output = output + chr(tmp)
        else:
            output = output + w
    print(output.lower())


def Playfair(ciphertxt, key):

    # 1. preprocess and try exception
    ciphertxt = ciphertxt.replace(" ", "").upper()
    for x in ciphertxt:
        if not x.isalpha():
            raise SystemExit(
                f"ciphertxt is invalid with the char: {x}")

    # 2.optional: create key table
    AtoZ = ''.join(chr(x) for x in range(65, 91))
    tmp = key.replace(" ", "").upper()+AtoZ
    keytable = ''
    for x in tmp:
        if not x in keytable and x.isalpha():
            keytable = keytable+x
    keytable = keytable.replace("J", "")

    # 3.decryted
    output = ""
    for pre in range(0, len(ciphertxt), 2):
        preIndex = keytable.index(ciphertxt[pre])
        postIndex = keytable.index(ciphertxt[pre+1])
        preRow, preCol = int(preIndex/5), preIndex % 5
        postRow, postCol = int(postIndex/5), postIndex % 5

        # same row 以左替代解密
        if postRow == preRow:

            if preCol == 0:
                preCol = 4
            else:
                preCol = preCol - 1
            if postCol == 0:
                postCol = 4
            else:
                postCol = postCol - 1

        # same col 以上替代解密
        elif postCol == preCol:
            if preRow == 0:
                preRow = 4
            else:
                preRow = preRow - 1
            if postRow == 0:
                postRow = 4
            else:
                postRow = postRow - 1
        # other 找四角同行替帶解密
        else:
            tmp = preCol
            preCol = postCol
            postCol = tmp

        output = output + keytable[preRow*5 + preCol]
        output = output + keytable[postRow*5 + postCol]

    print(output.lower())


def Vernam(ciphertxt, key):

    # 1. preprocess and check
    ciphertxt = ciphertxt.replace(" ", "").upper()
    for x in ciphertxt:
        if not x.isalpha():
            raise SystemExit(
                f"ciphertxt is invalid with the char: {x}")

    # 2. decrypt
    ikey = key.replace(" ", "").upper()
    output = ""
    for i in range(0, len(ciphertxt)):
        # xor key and ciphertxt
        tmp = ((ord(ikey[i])-ord('A')) ^
               (ord(ciphertxt[i])-ord('A')))+ord('A')
        output = output + chr(tmp)
        ikey = ikey + chr(tmp)
    # print(ikey)
    # print(ciphertxt)
    print(output.lower())


def Railfence(ciphertxt, key):
    # 1. preprocess and check
    # ciphertxt = ciphertxt.replace(" ", "").upper()
    # for x in ciphertxt:
    #     if not x.isalpha() and x != ' ' and x != ',' and x != '.':
    #         raise SystemExit(
    #             f"ciphertxt is invalid with the char: {x}")
    if key.isdigit():
        key = int(key)
    else:
        raise SystemExit(
            f"key is invalid with the char: {key}")

    # split string
     # len(str) 皆可表示為 n*(2k-2)+餘
    # \/\/ 理想整除 第一 中間 最後，切割字串的個數為 [n,2n,n]
    # \/\, 上殘型 [n+1, 2n+1~2n+2, n+1] 中間由前數來共 2k-2-餘個 2n+1
    # \/\/'下殘型 [n+1, 2n+1~2n+0, n]  中間由前數來 共 餘-1個 2n+1
    txtlen = len(ciphertxt)
    txtquo, txtmod = int(txtlen / (2 * key - 2)), txtlen % (2 * key - 2)
    txtTable = {}
    splitIndex = 0
    # idea-
    print(f"{txtlen}%{(2 * key - 2)} = {txtmod}")
    if txtmod == 0:
        _first, _mid, _last = (txtquo, txtquo*2, txtquo)
        modCount = 0
        modPlus = 0
    # 上殘
    elif txtmod >= key:
        _first, _mid, _last = (txtquo+1, txtquo*2+2, txtquo+1)
        modCount = 2*key - 2 - txtmod  # 1
        modPlus = -1
        print("==========")
    # 下殘
    else:
        _first, _mid, _last = (txtquo+1, txtquo*2, txtquo)
        modCount = txtmod-1
        modPlus = 1

    for i in range(0, key):
        if i == 0:
            splitNum = _first
        elif i == key-1:
            splitNum = _last
        else:
            if modCount != 0:
                splitNum = _mid+modPlus
                modCount = modCount-1
            else:
                splitNum = _mid
        print(f"modcount:{modCount}, modplus:{modPlus}")
        txtTable[i] = ciphertxt[splitIndex:splitIndex + splitNum]
        splitIndex = splitIndex + splitNum
        print(txtTable[i])

    # decrypt
    output = ''
    dir = 1  # 1 means down, -1 means up
    currentRow = 0
    for i in range(0, txtlen):
        tmpString = txtTable[currentRow]
        output = output + tmpString[0]
        txtTable[currentRow] = tmpString[1:]
        if currentRow == 0:
            dir = 1
        elif currentRow == key-1:
            dir = -1
        currentRow = currentRow + dir
    print(output)


def RowTransposition(ciphtxt, key):
    # preprocess

    chrNum = int(len(ciphertxt)/len(key))
    txtMod = (len(ciphertxt) % len(key))
    # print(chrNum)

    splitTxt = {}
    splitCount = 0
    keySorted = ''.join(sorted(key))
    for i in range(0, len(key)):
        # key 較前序的 在有餘數時 會多出1個字母
        if key.index(keySorted[i]) < txtMod:
            ltModNum = 1
        else:
            ltModNum = 0
        splitTxt[keySorted[i]] = ciphertxt[splitCount:splitCount+chrNum+ltModNum]
        splitCount = splitCount + chrNum+ltModNum
    # print(splitTxt)

    output = ''
    for i in key:
        print(splitTxt[i])
    for num in range(0, chrNum+1):
        for i in key:
            tmp = splitTxt[i]
            if num < len(tmp):
                output = output + tmp[num]
    print(output)


# py program.py -m .. -i .. -k ..
try:
    mindex = sys.argv[1:].index('-m')
    iindex = sys.argv[1:].index('-i')
    kindex = sys.argv[1:].index('-k')

except Exception as e:
    raise SystemExit(
        f"Usage: {sys.argv[0]} -m method -i ciphertxt -k key :)") from e

method = sys.argv[mindex+2]
ciphertxt = ' '.join(sys.argv[iindex+2:kindex+1])
key = ' '.join(sys.argv[kindex+2:])

# globals()[method](ciphertxt, key)
# try:
globals()[method](ciphertxt, key)
# except Exception as e:
#     raise SystemExit(f"method: {method} is non-defined, accepted method: Caesar,"
#                      'Playfair, Vernam, RailFence, RowTransposition') from e
