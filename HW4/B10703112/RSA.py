import sys
import random
import base64
MIN_PRIME = 2**511+1
MAX_PRIIME = 2**512-1
BIT_FILLUP_LEN = 350


def Miller_Rabin_Test(num: int, times):

    # input constraint: n>3 and odd
    if num == 2 or num == 3:
        return True
    if num % 2 == 0 or num == 1:
        return False

    # compute m where N-1 = 2^k*m
    k = 0
    m = num - 1
    while m % 2 == 0:
        m //= 2
        k += 1

    # choose a from [2:num-1],  b=(a^m) mod N
    for time in range(times):
        a = random.randrange(2, num-1)
        b = pow(a, m, num)
        if b != 1 and b != num-1:
            i = 1
            while i < k and b != num-1:
                b = pow(b, 2, num)
                if b == 1:
                    return False
                i += 1
            # false means composite by a
            if b != num-1:
                return False
    # True means propable prime
    return True


def setPrime():
    while(1):
        prime = random.randrange(MIN_PRIME, MAX_PRIIME)
        if Miller_Rabin_Test(prime, 25) == False:
            continue
        else:
            return prime


def GCD(a, b):
    while(b != 0):
        t = b
        b = a % b
        a = t
    return a


# e and m need to be co-prime, find Modular multiplicative inverse of e with modulo m
def getModularInverse(e, m):
    u1, u2, u3 = 1, 0, e
    v1, v2, v3 = 0, 1, m
    while v3 != 0:
        q = u3//v3
        v1, v2, v3, u1, u2, u3 = (u1-q*v1), (u2-q*v2), (u3-q*v3), v1, v2, v3
    return u1 % m


def ComputeKey(m):
    # find public key e, that e and modulo m is co-prime
    while(1):
        e = random.randrange(1, m)
        if GCD(e, m) != 1:
            continue
        else:
            break

    # find private key d, that is Modular multiplicative inverse of e with modulo m
    d = getModularInverse(e, m)

    return e, d


def key_generation():

    p = setPrime()
    q = setPrime()
    # compute N = p*q;  phi(N) = (p-1)(q-1)
    N = p*q
    phi = (p-1)*(q-1)

    # public key, private key, e*d % phi = 1
    e, d = ComputeKey(phi)

    if (e*d) % phi != 1:
        print("key error!!")

    print(f"p = {p}")
    print(f"q = {q}")
    print(f"N = {N}")
    print(f"phi = {phi}")
    print(f"e = {e}")
    print(f"d = {d}")
    return p, q, N, e, d


# y = x^exp % mod
def Square_and_Multiply(x: int, exp: int, mod: int):
    bi_exp = str(bin(int(exp)))
    y = x

    for i in range(3, len(bi_exp)):
        y = pow(y, 2, mod)
        if bi_exp[i] == '1':
            y = y*x % mod
    return y


def RSA_Encrypt(plaintText, N, e):

    ciphertext = ""
    for i in range(0, len(plaintText)):
        tmp = Square_and_Multiply(ord(plaintText[i]), e, N)
        # N avg 300~320bit, so fill up to 350bit
        ciphertext += (str(tmp)).rjust(BIT_FILLUP_LEN, '0')

    # BASE64 ENCODING
    ciphertext = base64.b64encode(ciphertext.encode("ascii")).decode("ascii")
    print(ciphertext)
    return ciphertext


def RSA_Decrypt(ciphertext, N, d):

    plaintText = ""
    # BASE64 DECODING
    ct = base64.b64decode(ciphertext.encode("ascii")).decode("ascii")
    for i in range(0, len(ct), BIT_FILLUP_LEN):
        tmp = Square_and_Multiply(int(ct[i:i+BIT_FILLUP_LEN]), d, N)
        plaintText += chr(tmp)
    print(plaintText)


def CRT_Decrypt(ciphertext, _p, _q, _d):

    plaintText = ""
    p = int(_p)
    q = int(_q)
    d = int(_d)
    d_Premainder = d % (p-1)
    d_Qremainder = d % (q-1)
    qinv = getModularInverse(q, p)

    ct = base64.b64decode(ciphertext.encode("ascii")).decode("ascii")

    for i in range(0, len(ct), BIT_FILLUP_LEN):
        #m1 = ciphertext[i]^d_Premainder % p
        m1 = Square_and_Multiply(
            int(ct[i:i+BIT_FILLUP_LEN]), d_Premainder, p)
        #m2 = ciphertext[i]^d_Qremainder % q
        m2 = Square_and_Multiply(
            int(ct[i:i+BIT_FILLUP_LEN]), d_Qremainder, q)
        h = qinv*(m1-m2) % p
        m = m2+h*q
        plaintText += chr(m)

    print(plaintText)


if "-i" in sys.argv:
    key_generation()

elif "-e" in sys.argv:
    tmp = sys.argv.index('-e')
    print(sys.argv)
    plaintText = sys.argv[tmp+1]
    N = sys.argv[tmp+2]
    e = sys.argv[tmp+3]
    RSA_Encrypt(plaintText, int(N), int(e))

elif "-d" in sys.argv:
    tmp = sys.argv.index('-d')
    ciphertext = sys.argv[tmp+1]
    N = sys.argv[tmp+2]
    d = sys.argv[tmp+3]
    RSA_Decrypt(ciphertext, int(N), int(d))

elif "-CRT" in sys.argv:
    tmp = sys.argv.index('-CRT')
    ciphertext = sys.argv[tmp+1]
    p = sys.argv[tmp+2]
    q = sys.argv[tmp+3]
    d = sys.argv[tmp+4]
    CRT_Decrypt(ciphertext, int(p), int(q), int(d))

else:
    print("no valid command to work\n")


# plaintText = "Info_Security_HW4"
# p, q, N, e, d = key_generation()
# ciphertext = RSA_Encrypt(plaintText, N, e)
# RSA_Decrypt(ciphertext, N, d)
# CRT_Decrypt(ciphertext, int(p), int(q), int(d))
