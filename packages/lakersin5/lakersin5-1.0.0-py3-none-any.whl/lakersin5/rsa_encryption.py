# lakersin5/rsa_encryption.py

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

def modinv(e, phi):
    return pow(e, -1, phi)

def generate_keys():
    # Small primes for demo; use larger ones in real-world
    p = 61
    q = 53
    n = p * q
    phi = (p - 1) * (q - 1)

    e = 17
    while gcd(e, phi) != 1:
        e += 2

    d = modinv(e, phi)
    return (e, n), (d, n)

def encrypt(plaintext, public_key):
    e, n = public_key
    return pow(plaintext, e, n)

def decrypt(ciphertext, private_key):
    d, n = private_key
    return pow(ciphertext, d, n)

def run_rsa_encryption_demo():
    print("\n=== RSA Encryption Demo ===")

    public_key, private_key = generate_keys()

    message = 42
    print(f"Original Message: {message}")

    cipher = encrypt(message, public_key)
    print(f"Encrypted: {cipher}")

    plain = decrypt(cipher, private_key)
    print(f"Decrypted: {plain}")

if __name__ == "__main__":
    run_rsa_encryption_demo()