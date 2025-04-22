# lakersin5/elgamal_signature.py

import hashlib

def modinv(a, m):
    return pow(a, -1, m)

def hash_message(msg):
    return int(hashlib.sha256(msg.encode()).hexdigest(), 16)

def sign(p, g, x, msg, k):
    H = hash_message(msg) % p
    r = pow(g, k, p)
    k_inv = modinv(k, p - 1)
    s = (k_inv * (H - x * r)) % (p - 1)
    return (r, s)

def verify(p, g, y, msg, signature):
    r, s = signature
    H = hash_message(msg) % p
    lhs = pow(y, r, p) * pow(r, s, p) % p
    rhs = pow(g, H, p)
    return lhs == rhs

def run_elgamal_signature_demo():
    print("\n=== ElGamal Signature Demo ===")

    # Params
    p = 467
    g = 2
    x = 127  # private key
    y = pow(g, x, p)  # public key
    k = 73   # random k (must be coprime with p-1)
    
    msg = "Hello ElGamal!"

    signature = sign(p, g, x, msg, k)
    print(f"Message: {msg}")
    print(f"Signature: {signature}")
    print("Valid Signature?" , verify(p, g, y, msg, signature))

if __name__ == "__main__":
    run_elgamal_signature_demo()