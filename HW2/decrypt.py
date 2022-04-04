import math
from pydoc import plain
import sys
#DES

def decrypt(cipher_text,key):
    # plaintext 跟 key 都是十六進制的
    cipher_text = cipher_text.replace('0x','')
    key = key.replace('0x','')
    cipher_text = hex_to_binary(cipher_text)
    key = hex_to_binary(key)
   

    #=========initial permutation==========#
    ip= (58, 50, 42, 34, 26, 18, 10, 2,
         60, 52, 44, 36, 28, 20, 12, 4,
         62, 54, 46, 38, 30, 22, 14, 6,
         64, 56, 48, 40, 32, 24, 16, 8,
         57, 49, 41, 33, 25, 17, 9 , 1,
         59, 51, 43, 35, 27, 19, 11, 3,
         61, 53, 45, 37, 29, 21, 13, 5,
         63, 55, 47, 39, 31, 23, 15, 7)
    #=========Final Permutation===========#
    ip_1=(40, 8, 48, 16, 56, 24, 64, 32,
          39, 7, 47, 15, 55, 23, 63, 31,
          38, 6, 46, 14, 54, 22, 62, 30,
          37, 5, 45, 13, 53, 21, 61, 29,
          36, 4, 44, 12, 52, 20, 60, 28,
          35, 3, 43, 11, 51, 19, 59, 27,
          34, 2, 42, 10, 50, 18, 58, 26,
          33, 1, 41, 9, 49, 17, 57, 25)

    #=========Key_PC_1 & PC_2===========#
    pc1=(57, 49, 41, 33, 25, 17, 9,
         1, 58, 50, 42, 34, 26, 18,
         10, 2, 59, 51, 43, 35, 27,
         19, 11, 3, 60, 52, 44, 36,
         63, 55, 47, 39, 31, 33, 15,
         7, 62, 54, 46, 38, 30, 22,
         14, 6, 61, 53, 45, 37, 29,
         21, 13, 5, 28, 20, 12, 4)

    pc2= (14, 17, 11, 24, 1, 5, 3, 28,
          15, 6, 21, 10, 23, 19, 12, 4, 
          26, 8, 16, 7, 27, 20, 13, 2, 
          41, 52, 31, 37, 47, 55, 30, 40, 
          51, 45, 33, 48, 44, 49, 39, 56, 
          34, 53, 46, 42, 50, 36, 29, 32)
    #==============E Bit-Selection Table============#
    e =(32, 1, 2, 3, 4, 5, 4, 5, 
        6, 7, 8, 9, 8, 9, 10, 11, 
        12,13, 12, 13, 14, 15, 16, 17,
        16,17, 18, 19, 20, 21, 20, 21,
        22, 23, 24, 25,24, 25, 26, 27, 
        28, 29,28, 29, 30, 31, 32, 1)
    

    #=====將key做PC1的移位=====#
    key_plus=''
    for i in range(0,len(pc1)):
        key_plus+=str(key[pc1[i]-1])
    ##print(key_plus)
    #=========================#

    #=====將key分為前半部跟後半部=====#
    C0 = key_plus[0:28]
    D0 = key_plus[28:56]
    ##print(C0)
    ##print(D0)

    #開始16輪的迭代 加密->左 解密->往右移動
    temp_C0=""
    temp_D0=""

    key_box_Left=[]
    key_box_Right=[]

    for i in range(1,17):
        if i == 1 or i == 2 or i == 9 or i == 16: #在2,9,16輪 往右邊移動一位
            # temp_C0+=C0[27:28] #最後一位跑到頭
            # temp_C0+=C0[0:27] #不包含最後一位
            # temp_D0+=D0[27:28] #最後一位跑到頭
            # temp_D0+=D0[0:27] #不包含最後一位
            temp_C0+=C0[1:28]
            temp_C0+=C0[0:1]
            temp_D0+=D0[1:28]
            temp_D0+=D0[0:1]

            key_box_Left.append(temp_C0)
            key_box_Right.append(temp_D0)
            C0 = temp_C0
            D0 = temp_D0
            temp_C0=""
            temp_D0=""
        else:
            # temp_C0+=C0[26:28] #其他情況下移動兩位
            # temp_C0+=C0[0:26]
            # temp_D0+=D0[26:28] #其他情況下移動兩位
            # temp_D0+=D0[0:26]

            temp_C0+=C0[2:28]
            temp_C0+=C0[0:2]
            temp_D0+=D0[2:28]
            temp_D0+=D0[0:2]
            key_box_Left.append(temp_C0)
            key_box_Right.append(temp_D0)
            C0 = temp_C0
            D0 = temp_D0
            temp_C0=""
            temp_D0=""
    #print(key_box)
    final_key_box=[] #放合成完的鑰匙

    for i in range(0,len(key_box_Left)):
        #print("左鑰匙: "+key_box_Left[i])
        #print("右鑰匙: "+key_box_Right[i])
        buffer = ""
        buffer += key_box_Left[i]+key_box_Right[i]

        #=====將key做PC2的移位=====#
        key_final=''
        for j in range(0,len(pc2)):
            key_final+=str(buffer[pc2[j]-1])
        ##print(buffer)  
        final_key_box.append(key_final)
        #print("\n")
    #print(len(key_box_Left))
    #print(len(key_box_Right))
    # for i in range(0,len(final_key_box)):
    #     print(len(final_key_box[i]))

    ##########################################

    #對資料IP移位
    data=""
    for i in range(0,len(ip)):
        data+=str(cipher_text[ip[i]-1])
    #print(data)

    L0 = data[0:32]
    R0 = data[32:64]
    #print(L0)
    #print(R0)

    sixteen_output=""
    L1=""
    R1=""

    for i in range(1,17):
        L1 = R0
        # R1 = L0 + f(R0,Key1)
        R1 = [ord(a)^ord(b) for a,b in zip(L0,f_function(R0,final_key_box[17-i-1]))]
        temp=""
        for j in range(0,len(R1)):
            temp+=str(R1[j])
        R1 = temp
        L0 = L1
        R0 = R1

        if i < 16:
            L1 = R1
    
    # print(type(L1))
    # print(type(R1))
    # print(L1)
    # print(R1)
    sixteen_output=str(R1)+str(L1)
    print(sixteen_output)

    
    # step = 8
    # b = [sixteen_output[i:i+step] for i in range(0,len(sixteen_output),step)]
    # print(b)

    #print(len(sixteen_output))

    # ip-1 的變換 #
    last=""
    for i in range(0,len(ip_1)):
        last += sixteen_output[ip_1[i]-1]
    print(last)

    step = 8
    b = [last[i:i+step] for i in range(0,len(last),step)]
    print(b)

    # 最後把last轉換成16進制
    bin_to_hex=[]
    temp1=""

    for i in range(0,len(last)):
        if i % 4!=0 or i==0:
            temp1+=str(last[i])
        else:
            bin_to_hex.append(temp1)
            temp1=str(last[i]) #

    bin_to_hex.append(temp1)

    #print(bin_to_hex)
    plaintext=""

    for i in range(0,len(bin_to_hex)):
        buf = hex(int(bin_to_hex[i],2))
        buf = buf.replace('0x','')
        plaintext+=buf

    
        
    # print(str.upper(plaintext))
    return str.upper(plaintext)
        

    



    #a = f_function(R0,final_key_box[0])
    #print (a)
    # temp_sbox=""
    # sbox=[]
    # for i in range(0,len(a)):
    #     if i % 6!=0 or i==0:
    #         temp_sbox+=str(a[i])
    #     else:
    #         sbox.append(temp_sbox)
    #         temp_sbox=str(a[i]) #
    # sbox.append(temp_sbox)
    # print(sbox)
    # sbox_output=[]

    # for i in range (0,len(sbox)):
    #     target = sbox[i]
    #     row = str(target[0])+str(target[5])
    #     row = int(row,2)
    #     column = str(target[1])+str(target[2])+str(target[3])+str(target[4])
    #     column = int(column,2)

    #     output = s[i][row][column]
    #     output = bin(output)
    #     output = output.replace('0b','')
    #     if len(output) < 4:
    #         temp=''
    #         for i in range(0,4-len(output)):
    #             temp+="0"
    #         output=temp+output

    #     sbox_output.append(output)

    # print(sbox_output)

def hex_to_binary(cipher_text):
    outcome=''
    length=len(cipher_text)
    length = length % 16 #看是不是皆為16個位元組
    if length != 0:
        buffer=''
        for i in range(0,16-length):
            buffer+='0'
        cipher_text+=buffer

    
    for i in cipher_text:
        code_ord = int(i,16)
        #print(code_ord)
        binary_code = bin(code_ord) #轉換成二進制
        binary_code=binary_code.replace('0b','') #把前面的0b刪掉
        #如果轉為binary小於4位數 則補0
        if len(binary_code) < 4:
            temp=''
            for i in range(0,4-len(binary_code)):
                temp+="0"
            binary_code=temp+binary_code
        #print(binary_code)
        outcome+=binary_code
    return outcome
    
    
def f_function(R,key):
    #==============E Bit-Selection Table============#
    e =(32, 1, 2, 3, 4, 5, 4, 5, 
        6, 7, 8, 9, 8, 9, 10, 11, 
        12,13, 12, 13, 14, 15, 16, 17,
        16,17, 18, 19, 20, 21, 20, 21,
        22, 23, 24, 25,24, 25, 26, 27, 
        28, 29,28, 29, 30, 31, 32, 1)
    ################### S1 ~ S8 #####################

    s=[ [[14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
        [0, 15, 7, 4, 14, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
        [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
        [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]],
        [[15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
        [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
        [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
        [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]],
        [[10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
        [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
        [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
        [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]],
        [[7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
        [13, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14,9],
        [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
        [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]],
        [[2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
        [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
        [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
        [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]],
        [[12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
        [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
        [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
        [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]],
        [[4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
        [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
        [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
        [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]],
        [[13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
        [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
        [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
        [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]]]

    #========================變換P矩陣======================#
    p=(16, 7, 20, 21, 29, 12, 28, 17,
        1, 15, 23, 26, 5, 18, 31, 10, 
        2, 8, 24, 14, 32, 27, 3, 9,
        19, 13, 30, 6, 22, 11, 4, 25)
    
    Expansion_R=""
    for i in range(0,len(e)):
        Expansion_R+=str(R[e[i]-1])
    #print(Expansion_R)
    #print(key)
    xor_outcome = [ord(a)^ord(b) for a,b in zip(Expansion_R,key)]

    #return xor_outcome


    temp_sbox=""
    sbox=[]
    for i in range(0,len(xor_outcome)):
        if i % 6!=0 or i==0:
            temp_sbox+=str(xor_outcome[i])
        else:
            sbox.append(temp_sbox)
            temp_sbox=str(xor_outcome[i]) #
    sbox.append(temp_sbox)
    #print(sbox)
    sbox_output=[]
    sbox_str=""

    for i in range (0,len(sbox)):
        target = sbox[i]
        row = str(target[0])+str(target[5])
        row = int(row,2)
        column = str(target[1])+str(target[2])+str(target[3])+str(target[4])
        column = int(column,2)

        output = s[i][row][column]
        output = bin(output)
        output = output.replace('0b','')
        if len(output) < 4:
            temp=''
            for i in range(0,4-len(output)):
                temp+="0"
            output=temp+output

        sbox_output.append(output)
        sbox_str+=output

    Final_process=""

    #return sbox_output
    for i in range(0,len(p)):
        Final_process+=str(sbox_str[p[i]-1])
    return Final_process



#hex_to_binary('0123456789ABCDEF1')
#print(hex_to_binary('133457799BBCDFF1'))
#decrypt('C0999FDDE378D7ED','0E329232EA6D0D73')
print(sys.argv)
iindex = sys.argv.index('-i')
kindex = sys.argv.index('-k')

if '-i' in sys.argv:
    print('yess')

input = ' '.join(sys.argv[iindex+1:kindex])
key = ' '.join(sys.argv[kindex+1:])


out = decrypt(input, key)
tmp = '0x'+hex(int(out, 2))[2:].upper()
print(tmp)

