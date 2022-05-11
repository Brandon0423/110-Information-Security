from re import X
import random
import math
import base64
import sys
from itsdangerous import base64_encode
from numpy import arange


def isprime(number):
    if number == 2 or number == 3:
        return True
    if number % 2 == 0 or number < 2:
        return True
    for i in range(3, int(number**0.5)+1, 2):
        if number % i == 0:
            return False
    return True

# 檢查是否互質


def gcd(a, b):
    if(b == 0):
        return a
    else:
        return gcd(b, a % b)


def getPrime():
    Min = 2**511+1
    Max = 2**512-1
    while(1):
        p = random.randrange(Min, Max)
        if Miller_Rabin(p, 20) == False:
            continue
        else:
            return p


def Miller_Rabin(number, iterated_time):
    if number == 2 or number == 3:
        return True
    if number % 2 == 0 or number == 1:
        return False
    k = 0
    m = number-1
    while m % 2 == 0:
        k += 1
        m //= 2

    for i in range(iterated_time):
        a = random.randrange(2, number-1)
        # bo = a^m(modn)
        x = pow(a, m, number)
        if x == 1 or x == number-1:
            continue
        for j in range(k-1):
            x = pow(x, 2, number)
            if x == number-1:
                break
        else:
            return False
    return True

# Square 加速 # 2^n%d


def Square_multiply(x, exp, n):
    binary_exp = str(bin(int(exp)))
    # print(binary_exp)
    y = x

    for i in range(3, len(binary_exp)):
        y = y**2 % int(n)
        if binary_exp[i] == '1':
            y = y*x % int(n)
    return y


def findModReverse(a, m):  # 找inverse

    if gcd(a, m) != 1:
        return None
    u1, u2, u3 = 1, 0, a
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3//v3
        v1, v2, v3, u1, u2, u3 = (u1-q*v1), (u2-q*v2), (u3-q*v3), v1, v2, v3
    return u1 % m


def RSA_generation():
    # 質數p,q
    p = getPrime()
    q = getPrime()
    # N
    N = p*q

    # 歐拉函數
    phi = (p-1)*(q-1)

    # 公鑰
    while(1):
        e = random.randrange(1, phi)
        if gcd(e, phi) != 1:
            continue
        else:
            break
    # 私鑰
    #d = (e-1) % phi
    d = findModReverse(e, phi)

    output = []
    output.append(p)
    output.append(q)
    output.append(N)
    output.append(phi)
    output.append(e)
    output.append(d)
    print("p = ", p)
    print("q = ", q)
    print("N = ", N)
    print("phi = ", phi)
    print("e = ", e)
    print("d = ", d)
    return output


def RSA_encryption(message, N, e):  # 信息, N ,公鑰
    #output = []
    ciphertext = ""
    for i in range(0, len(message)):
        #encry = (ord(message[i]) ** e % N)
        encry = Square_multiply(ord(message[i]), e, N)
        encry_temp = str(encry)
        encry_temp = encry_temp.rjust(500, '0')
        # print(len(encry_temp))
        #print("現在的字母是: ",encry_temp)
        #encry = exp_func(ord(message[i]), e)
        #encry = encry % N
        temp = str(encry_temp)
        # output.append(encry)
        ciphertext += temp
    #encry = Square_multiply(message,e,)
    #print("前:   ",ciphertext)
    b = ciphertext.encode("ascii")
    base64_bytes = base64.b64encode(b)
    base64_string = base64_bytes.decode("ascii")

    print(base64_string)
    # return output


def RSA_decryption(ciphertext, N, d):

    print(type(ciphertext))
    base64_message = ciphertext
    base64_bytes = base64_message.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('ascii')
    #print("訊息是:", message)

    output = ""
    buffer = ""
    counter = 0
    for i in range(0, len(message)):
        if counter == 500:
            print("要解密的東西是:", buffer)
            # print(len(buffer))
            data = int(buffer)
            print("處理完後長這樣: ", data)
            decry = chr(Square_multiply(data, d, N))
            print("平方加速後: ", decry)
            output += str(decry)
            counter = 1
            buffer = message[i]
        else:
            buffer += message[i]
            counter += 1

    last_word = int(message[-500:len(message)])
    print("最後字 :" ,last_word)
    decry = chr(Square_multiply(last_word, d, N))
    print("平方加速後: ", decry)
    output += str(decry)

    print(output)

    # for i in range(0, len(ciphertext)):
    #     #decry = chr(ciphertext[i] ** d % N)
    #     decry = chr(Square_multiply(ciphertext[i], d, N))
    #     #decry = exp_func(ciphertext[i], d)
    #     #decry = chr(decry % N)
    #     temp = str(decry)
    #     output += temp
    print(output)


def CRT_decryption(ciphertext, p, q, d):

    base64_message = ciphertext
    base64_bytes = base64_message.encode('ascii')
    message_bytes = base64.b64decode(base64_bytes)
    message = message_bytes.decode('ascii')

    output = ""
    p = int(p)
    q = int(q)
    d = int(d)
    dp = d % (p-1)
    dq = d % (q-1)
    qinv = findModReverse(q, p)
    
    box=[]
    buffer = ""
    counter = 0
    for i in range(0, len(message)):
        if counter == 500:
            
            print("要解密的東西是:", buffer)
            # print(len(buffer))
            data = int(buffer)
            print("處理完後長這樣: ", data)
            box.append(data)
            counter = 1
            buffer = message[i]
        else:
            buffer += message[i]
            counter += 1
    last_word = int(message[-500:len(message)])
    box.append(last_word)


    # for i in range(0, len(ciphertext)):
    #     #m1 = ciphertext[i]**dp % p
    #     m1 = Square_multiply(ciphertext[i], dp, p)
    #     #m2 = ciphertext[i]**dq % q
    #     m2 = Square_multiply(ciphertext[i], dq, q)
    #     h = qinv*(m1-m2) % p
    #     m = m2+h*q
    #     output += chr(m)


    for i in range(0, len(box)):
        #m1 = ciphertext[i]**dp % p
        m1 = Square_multiply(box[i], dp, p)
        #m2 = ciphertext[i]**dq % q
        m2 = Square_multiply(box[i], dq, q)
        h = qinv*(m1-m2) % p
        m = m2+h*q
        output += chr(m)

    print(output)


#temp = RSA_generation()
# for i in range(0,len(temp)):
#     print(temp[i])

message = "justinbieber"

# ciphertext = RSA_encryption(message, temp[2], temp[4])
# RSA_decryption(ciphertext, temp[2], temp[5])
# CRT_decryption(ciphertext, temp[0], temp[1], temp[5])


def main(args):
    generation = []
    if "-i" in args:
        generation = RSA_generation()
        return
    if "-e" in args:
        if len(args) != 4:
            print("Wrong Format")
            return
        message = args[1]
        N = args[2]
        e = args[3]
        RSA_encryption(message, N, e)
        return
    if "-d" in args:
        if len(args) != 4:
            print("Wrong Format")
            return
        cipher = args[1]
        N = args[2]
        d = args[3]
        RSA_decryption(cipher, N, d)
        return
    if "-CRT" in args:
        if len(args) != 5:
            print("Wrong Format")
            return
        cipher = args[1]
        p = args[2]
        q = args[3]
        d = args[4]
        CRT_decryption(cipher, p, q, d)
        return


if __name__ == "__main__":
    main(sys.argv[1:])
