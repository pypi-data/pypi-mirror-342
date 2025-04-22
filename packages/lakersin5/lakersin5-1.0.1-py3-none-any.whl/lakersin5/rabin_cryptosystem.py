# lakersin5/rabin_cryptosystem.py

def encrypt(m, n):
    return (m * m) % n

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def modinv(a, m):
    return pow(a, -1, m)

def chinese_remainder_theorem(a1, p, a2, q):
    n = p * q
    m1 = q
    m2 = p
    inv1 = modinv(q, p)
    inv2 = modinv(p, q)
    return (a1 * m1 * inv1 + a2 * m2 * inv2) % n

def decrypt(c, p, q):
    n = p * q

    # Compute square roots modulo p and q
    r1 = pow(c, (p + 1) // 4, p)
    r2 = pow(c, (q + 1) // 4, q)

    # 4 possible roots using CRT
    root1 = chinese_remainder_theorem(r1, p, r2, q)
    root2 = chinese_remainder_theorem(p - r1, p, r2, q)
    root3 = chinese_remainder_theorem(r1, p, q - r2, q)
    root4 = chinese_remainder_theorem(p - r1, p, q - r2, q)

    return (root1, root2, root3, root4)

def run_rabin_cryptosystem_demo():
    print("\n=== Rabin Cryptosystem Demo ===")

    p = 7
    q = 11
    n = p * q

    message = 20
    print(f"Original Message: {message}")

    cipher = encrypt(message, n)
    print(f"Encrypted: {cipher}")

    roots = decrypt(cipher, p, q)
    print(f"Decryption (4 possible roots): {roots}")

if __name__ == "__main__":
    run_rabin_cryptosystem_demo()