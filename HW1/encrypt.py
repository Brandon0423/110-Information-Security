import numpy as np
import sys


def Caesar(plaintext, key):

    outcome = ''

    for i in plaintext:
        if i.isalpha():  # 如果i是字母
            num = ord(i)
            num += int(key)

            if i.isupper():
                if num > ord('Z'):
                    num -= 26
                elif num < ord('A'):
                    num += 26
            elif i.islower():
                if num > ord('z'):
                    num -= 26
                elif num < ord('a'):
                    num += 26
            outcome += chr(num)
        else:
            outcome += i

    print(outcome)


def playfair(plaintext, key):

    board_chr = "abcdefghijklmnopqrstuvwxyz"
    plaintext = plaintext.replace(' ', '')
    processed_key = ""  # 把重複的元素刪掉
    for element in key:
        if element not in processed_key:
            processed_key += str(element)
    processed_key = processed_key.replace(' ', '')  # 把多餘的空格刪掉
# print(processed_key)

    temp = board_chr

    for i in range(len(board_chr)):
        for j in range(len(processed_key)):
            if processed_key[j] == 'i' and board_chr[i] == processed_key[j]:  # 需要連同j一起刪掉
                temp = temp.replace(temp[i], " ")
                temp = temp.replace(temp[i+1], " ")
            elif processed_key[j] == 'j' and board_chr[i] == processed_key[j]:  # 需要連同i一起刪掉
                temp = temp.replace(temp[i], " ")
                temp = temp.replace(temp[i-1], " ")
            elif board_chr[i] == processed_key[j]:
                temp = temp.replace(temp[i], " ")

    for i in range(len(temp)):
        if temp[i] == 'i':
            temp = temp.replace('j', '')
            break

    temp = temp.replace(' ', '')  # 把空格刪掉
    # print(temp)

    Fullboard = processed_key + temp

    column, row = 5, 5

    matrix = [[0 for _ in range(row)] for _ in range(column)]  # 把matrix用0填滿

    count = 0

    for i in range(0, 5):
        for j in range(0, 5):
            matrix[i][j] = Fullboard[count]
            count = count+1

    # print(matrix)

############################ 處理輸入的資料 ###################################

    boxbox = []

    for i in range(0, len(plaintext)):
        boxbox.append(plaintext[i])

    plaintext = ""
    for i in range(0, len(boxbox)):
        if boxbox[i] == 'j':
            boxbox[i] = 'i'
        plaintext += boxbox[i]

    string_box = []

    buffer = ""

    def cut_string(plaintext, box):
        buffer = ""

        if len(plaintext) == 0:
            return 0
        elif len(plaintext) == 1:
            plaintext = plaintext+"x"
        if plaintext[0] == plaintext[1] and len(plaintext) != 0:
            new_string = ""
            buffer = plaintext[0]+"x"
            box.append(buffer)

            for i in range(0, len(plaintext)):
                if i != 0:
                    new_string += plaintext[i]
        # plaintext=plaintext.replace(plaintext[0],'') #把第一位置刪掉
            if len(new_string) == 1:
                new_string += "x"
            buffer = ""
            cut_string(new_string, box)  # 繼續recursive

        elif plaintext[0] != plaintext[1] and len(plaintext) != 0:
            new_string = ""
            buffer = plaintext[0]+plaintext[1]
            box.append(buffer)
            buffer = ""
            for i in range(0, len(plaintext)):
                if i != 0 and i != 1:
                    new_string += plaintext[i]
        # plaintext=plaintext.replace(plaintext[0],'')
        # plaintext=plaintext.replace(plaintext[1],'')
            cut_string(new_string, box)

    cut_string(plaintext, string_box)

    # print(string_box)


################################################################

# 開始加密 :

    def playfair_cipher(matrix, letter1, letter2):

        # letter1_posx,letter1_posy = 0 #第一個字母的位置
        # letter2_posx,letter2_posy = 0 #第二個字母的位置

        for i in range(0, 5):
            for j in range(0, 5):
                if letter1 == matrix[i][j]:
                    letter1_posx = i
                    letter1_posy = j
                    break
        for i in range(0, 5):
            for j in range(0, 5):
                if letter2 == matrix[i][j]:
                    letter2_posx = i
                    letter2_posy = j
                    break

        outcome = ""
    # Rectangle
        if letter1_posx != letter2_posx and letter1_posy != letter2_posy:
            outcome += matrix[letter1_posx][letter2_posy]
            outcome += matrix[letter2_posx][letter1_posy]
    # 同一橫行
        elif letter1_posx == letter2_posx:
            if letter1_posy+1 > 4:
                letter1_posy = 0
            else:
                letter1_posy += 1

            if letter2_posy+1 > 4:
                letter2_posy = 0
            else:
                letter2_posy += 1

            outcome += matrix[letter1_posx][letter1_posy]
            outcome += matrix[letter2_posx][letter2_posy]

    # 同一直行
        elif letter1_posy == letter2_posy:
            if letter1_posx+1 > 4:
                letter1_posx = 0
            else:
                letter1_posx += 1

            if letter2_posx+1 > 4:
                letter2_posx = 0
            else:
                letter2_posx += 1

            outcome += matrix[letter1_posx][letter1_posy]
            outcome += matrix[letter2_posx][letter2_posy]

        return outcome
    output = ""
    for i in range(len(string_box)):
        #print(playfair_cipher(matrix, string_box[i][0], string_box[i][1]))
        output += playfair_cipher(matrix, string_box[i][0], string_box[i][1])
    print(output)


def Rail_Fence(plaintext, key):
    key = int(key)
    matrix = [[0 for _ in range(0, len(plaintext))]
              for _ in range(0, key)]  # 前面是Row 後面是Column
    # print(matrix)

    list = []

    for i in range(0, key):
        list.append(i)
        # print(i)

    flag = 0  # 檢查是否觸底
    count = 0

    for j in range(0, len(plaintext)):
        matrix[count][j] = plaintext[j]
        # print(matrix)

        if count == key-1:
            flag = 1
        elif count == 0:
            flag = 0

        # if count == 0:

        if flag == 0:
            count = count+1
            if count > 2:
                count = 2
        elif flag == 1:
            count = count-1
            if count < 0:
                count = 0

        Cipher_text = ""

    for i in range(0, key):
        for j in range(0, len(plaintext)):
            if matrix[i][j] != 0:
                Cipher_text += matrix[i][j]

    print(Cipher_text)
    # return matrix


def Row_Transposition_Cipher(plaintext, key):

    length = len(key)

    row = length
    column = len(plaintext)/length

    if column > int(column):
        column = int(column+1)
    else:
        column = int(column)

    matrix = np.zeros((column, row), dtype=np.str0)
# print(matrix)

    row1 = column
    column1 = row

    count = 0
    flag = 0

    dic = {}
    list1 = []

    for i in range(0, len(key)):
        list1.append(key[i])

    list1.sort()  # a,c,h,k
    # print(list1)

    for i in range(0, len(list1)):
        dic[list1[i]] = i

    # print(dic)  # {'a': 0, 'c': 1, 'h': 2, 'k': 3}

    list_of_keys = dic.keys()
    list_of_keys = list(list_of_keys)  # 把key轉為列表

# list_of_values=dic.values()
# list_of_values=list(list_of_values) #把value轉為列表

    position_dic = {}

    for i in range(0, len(key)):
        position_dic[key[i]] = i
    # print(position_dic)  # {'h': 0, 'a': 1, 'c': 2, 'k': 3}

    for i in range(0, row1):
        if flag == 1:
            break
        for j in range(0, column1):
            matrix[i][j] = plaintext[count]
            count = count+1
            if count >= len(plaintext):
                flag = 1
                break
    # print(matrix)
# [['g' 'e' 'e' 'k']
#['s' ' ' 'f' 'o']
#['r' ' ' 'g' 'e']
# ['e' 'k' 's' '']]
    output = ""
    for j in range(0, len(list_of_keys)):
        for k in range(0, row1):
            temp = position_dic[list_of_keys[j]]  # 查位置 a最先開始 並對到第一行，所以先印第一行
        # 下一個進來的是c 對應到pos裡面的第二行
        # 再來是h對應到裡面的第0行
        # 最後是k 對應到第4行
            output += matrix[k][temp]
            # print(matrix[k][temp])
    print(output)


def Vernam(plaintext, key):

    plaintext = plaintext.replace(" ", "")
    if len(key) < len(plaintext):
        key = key + plaintext[0:len(plaintext)-len(key)]
    #key = key.replace(" ","")
    outcome = ""

    for i in range(0, len(plaintext)):
        # plaintext_ord = ord(plaintext(i)-ord('A'))
        # key_ord = ord(key[i])-ord('A')
        # temp = (plaintext_ord^key_ord) + ord('A')
        temp = ((ord(plaintext[i])-ord('A')) ^ (ord(key[i])-ord('A')))+ord('A')
        outcome = outcome + chr(temp)

    print(outcome)


mindex = sys.argv[1:].index('-m')
iindex = sys.argv[1:].index('-i')
kindex = sys.argv[1:].index('-k')

method = sys.argv[mindex+2]
plaintext = ' '.join(sys.argv[iindex+2:kindex+1])
key = ' '.join(sys.argv[kindex+2:])

globals()[method](plaintext, key)
