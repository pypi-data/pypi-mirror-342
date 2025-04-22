# lakersin5/rsa_signature.py

import hashlib

def modinv(e, phi):
    return pow(e, -1, phi)

def hash_message(msg):
    return int(hashlib.sha256(msg.encode()).hexdigest(), 16)

def generate_keys():
    p = 61
    q = 53
    n = p * q
    phi = (p - 1) * (q - 1)

    e = 17
    d = modinv(e, phi)

    return (e, n), (d, n)

def sign(message, private_key):
    d, n = private_key
    hashed = hash_message(message)
    return pow(hashed, d, n)

def verify(message, signature, public_key):
    e, n = public_key
    hashed = hash_message(message)
    check = pow(signature, e, n)
    return hashed % n == check

def run_rsa_signature_demo():
    print("\n=== RSA Digital Signature Demo ===")

    public_key, private_key = generate_keys()

    message = "RSA is powerful!"
    signature = sign(message, private_key)

    print(f"Message: {message}")
    print(f"Signature: {signature}")
    print("Valid Signature?", verify(message, signature, public_key))

if __name__ == "__main__":
    run_rsa_signature_demo()