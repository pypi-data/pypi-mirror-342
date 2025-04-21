# lakersin5/full_des_using_pycryptodome.py
from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes

def des_encrypt(plaintext, key):
    cipher = DES.new(key, DES.MODE_ECB)
    return cipher.encrypt(plaintext)

def des_decrypt(ciphertext, key):
    cipher = DES.new(key, DES.MODE_ECB)
    return cipher.decrypt(ciphertext)

def run_full_des_demo():
    print("\n=== Full DES (using pycryptodome) Demo ===")

    # Generate random 8-byte key for DES (56-bit effective key)
    key = get_random_bytes(8)

    # Example plaintext (must be a multiple of 8 bytes)
    plaintext = b'ABCDEFGH'  # 8 bytes

    print(f"Key:       {key.hex()}")
    print(f"Plaintext: {plaintext}")

    ciphertext = des_encrypt(plaintext, key)
    print(f"Ciphertext: {ciphertext.hex()}")

    decrypted = des_decrypt(ciphertext, key)
    print(f"Decrypted:  {decrypted.decode()}")

if __name__ == "__main__":
    run_full_des_demo()