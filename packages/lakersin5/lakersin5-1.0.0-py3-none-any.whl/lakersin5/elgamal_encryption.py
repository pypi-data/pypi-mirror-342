# lakersin5/elgamal_encryption.py

def modexp(base, exp, mod):
    result = 1
    base %= mod
    while exp:
        if exp % 2:
            result = (result * base) % mod
        base = (base * base) % mod
        exp //= 2
    return result

def encrypt(p, g, y, m, k):
    a = modexp(g, k, p)
    b = (m * modexp(y, k, p)) % p
    return (a, b)

def decrypt(p, x, a, b):
    s = modexp(a, x, p)
    s_inv = pow(s, -1, p)
    m = (b * s_inv) % p
    return m

def run_elgamal_encryption_demo():
    print("\n=== ElGamal Encryption Demo ===")
    
    # Public params
    p = 467  # large prime
    g = 2    # generator

    # Keys
    x = 127  # private key
    y = modexp(g, x, p)  # public key

    m = 123  # message to encrypt
    k = 73   # ephemeral key

    print(f"Message: {m}")
    a, b = encrypt(p, g, y, m, k)
    print(f"Ciphertext: (a={a}, b={b})")

    decrypted = decrypt(p, x, a, b)
    print(f"Decrypted message: {decrypted}")

if __name__ == "__main__":
    run_elgamal_encryption_demo()