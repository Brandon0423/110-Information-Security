import sys
import numpy as np
from sklearn import exceptions


# KEY正向左 負向右 (解密) A65 90 a97 122
def caesar(ciphertxt, key):
    output = ""
    try:
        ikey = int(key) % 26
    except Exception as e:
        raise SystemExit(
            f"Caesar key is invalid: {key} ") from e

    for w in ciphertxt:
        if w.isalpha():
            num = ord(w)
            num = num - ikey

            if w.isupper():
                if num > ord('Z'):
                    num = num - 26
                elif num < ord('A'):
                    num = num + 26

            if w.islower():
                if num > ord('z'):
                    num = num - 26
                elif num < ord('a'):
                    num = num + 26
            output = output + chr(num)
        else:
            output = output + w
    print(output)


def playfair(ciphertxt, key):

    # 1. preprocess and try exception
    ciphertxt = ciphertxt.replace(" ", "").upper()
    for x in ciphertxt:
        if not x.isalpha():
            raise SystemExit(
                f"ciphertxt is invalid with the char: {x}")

    # 2. create key table
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

    print(output)


def vernam(ciphertxt, key):
    ciphertxt = ciphertxt.upper()
    if len(key) < len(ciphertxt):
        ikey = key + ciphertxt[0:len(ciphertxt)-len(key)]

    output = ""
    for i in range(0, len(ciphertxt)):
        # xor key and ciphertxt
        tmp = ((ord(ikey[i])-ord('A')) ^
               (ord(ciphertxt[i])-ord('A'))) + ord('A')
        # print(tmp)
        output = output + chr(tmp)
    # print(ikey)
    # print(ciphertxt)
    print(output)


def railfence(ciphertxt, key):
    # 1. preprocess and check
    ciphertxt = ciphertxt.replace(" ", "")
    if key.isdigit():
        key = int(key)
    else:
        raise SystemExit(
            f"key: {key} is invalid")

    # split string
    # len(str) 皆可表示為 n*(2k-2)+餘
    # \/\/ 理想整除 第一 中間 最後，切割字串的個數為 [n,2n,n]
    # \/\, 上殘型 [n+1, 2n+1~2n+2, n+1] 中間由前數來共 (2k-2-餘) 個 2n+1
    # \/\/'下殘型 [n+1, 2n+1~2n+0, n]  中間由前數來 共 (餘-1) 個 2n+1
    txtlen = len(ciphertxt)
    txtquo, txtmod = int(txtlen / (2 * key - 2)), txtlen % (2 * key - 2)  # n,餘
    # idea-
    if txtmod == 0:
        _first, _mid, _last = (txtquo, txtquo*2, txtquo)
        modCount = 0
        modPlus = 0
    # 上殘
    elif txtmod >= key:
        _first, _mid, _last = (txtquo+1, txtquo*2+2, txtquo+1)
        modCount = 2*key - 2 - txtmod
        modPlus = -1
    # 下殘
    else:
        _first, _mid, _last = (txtquo+1, txtquo*2, txtquo)
        modCount = txtmod-1
        modPlus = 1
    txtTable = {}
    splitIndex = 0
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
        txtTable[i] = ciphertxt[splitIndex:splitIndex + splitNum]
        splitIndex = splitIndex + splitNum

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


def row(ciphtxt, key):
    # preprocess

    chrNum = int(len(ciphertxt)/len(key))
    txtMod = (len(ciphertxt) % len(key))
    # print(chrNum)

    splitTxt = {}
    splitCount = 0
    keySorted = ''.join(sorted(key))
    for i in range(0, len(key)):
        # key 較前序的(共餘數個) 會多分1個字母
        if key.index(keySorted[i]) < txtMod:
            ltModNum = 1
        else:
            ltModNum = 0
        splitTxt[keySorted[i]] = ciphertxt[splitCount:splitCount+chrNum+ltModNum]
        splitCount = splitCount + chrNum+ltModNum
    # print(splitTxt)

    output = ''
    # for i in key:
    # print(splitTxt[i])
    for num in range(0, chrNum+1):
        for i in key:
            tmp = splitTxt[i]
            if num < len(tmp):
                output = output + tmp[num]
    print(output)


# py program.py -m .. -i .. -k ..
try:
    # print(sys.argv)
    mindex = sys.argv[1:].index('-m')
    iindex = sys.argv[1:].index('-i')
    kindex = sys.argv[1:].index('-k')

except Exception as e:
    raise SystemExit(
        f"Usage: {sys.argv[0]} -m method -i ciphertxt -k key, check command :)") from e

method = sys.argv[mindex+2]
ciphertxt = ' '.join(sys.argv[iindex+2:kindex+1])
key = ' '.join(sys.argv[kindex+2:])

# globals()[method](ciphertxt, key)


if method != 'caesar' and method != 'playfair' and method != 'vernam' and method != 'railfence' and method != 'row':
    raise SystemExit(f"method: {method} is non-defined, accepted method: caesar,"
                     'playfair, vernam, railfence, row')

globals()[method](ciphertxt, key)
