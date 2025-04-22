# lakersin5/aes.py
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

def aes_encrypt(plaintext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    return cipher.encrypt(pad(plaintext, AES.block_size))

def aes_decrypt(ciphertext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted = cipher.decrypt(ciphertext)
    return unpad(decrypted, AES.block_size)

def run_aes_demo():
    print("\n=== AES Encryption/Decryption Demo ===")

    # Generate a random 256-bit key for AES
    key = get_random_bytes(32)  # AES-256
    print(f"Key:       {key.hex()}")

    # Example plaintext (must be padded to block size)
    plaintext = b'KingJames!'

    print(f"Plaintext: {plaintext}")

    # Encrypt the plaintext
    ciphertext = aes_encrypt(plaintext, key)
    print(f"Ciphertext: {ciphertext.hex()}")

    # Decrypt the ciphertext
    decrypted = aes_decrypt(ciphertext, key)
    print(f"Decrypted:  {decrypted.decode()}")

if __name__ == "__main__":
    run_aes_demo()