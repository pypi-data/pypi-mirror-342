import random
from math import pow

def gcd(a, b):
    if a < b:
        return gcd(b, a)
    elif a % b == 0:
        return b
    else:
        return gcd(b, a % b)

def gen_key(q):
    key = random.randint(pow(10, 20), q)
    while gcd(q, key) != 1:
        key = random.randint(pow(10, 20), q)
    return key

def power(a, b, c):
    x = 1
    y = a
    while b > 0:
        if b % 2 != 0:
            x = (x * y) % c
        y = (y * y) % c
        b = int(b / 2)
    return x % c

def encrypt(msg, q, h, g):
    en_msg = []
    k = gen_key(q)
    s = power(h, k, q)
    p = power(g, k, q)
    
    for i in range(len(msg)):
        en_msg.append(s * ord(msg[i]))

    return en_msg, p

def decrypt(en_msg, p, key, q):
    dr_msg = []
    h = power(p, key, q)
    for i in range(len(en_msg)):
        dr_msg.append(chr(int(en_msg[i] / h)))
    return dr_msg

def main():
    msg = input("Enter the message to encrypt: ")
    q = int(input("Enter a large prime number (q): "))
    g = int(input(f"Enter a generator (g) between 2 and {q-1}: "))
    
    key = gen_key(q)
    h = power(g, key, q)
    
    en_msg, p = encrypt(msg, q, h, g)
    dr_msg = decrypt(en_msg, p, key, q)
    dmsg = ''.join(dr_msg)
    print("Decrypted Message:", dmsg)

if __name__ == '__main__':
    main()