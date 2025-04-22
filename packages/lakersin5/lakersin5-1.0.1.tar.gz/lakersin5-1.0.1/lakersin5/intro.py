from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import random

# Function to check if a number is prime
def is_prime(num):
    if num < 2:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True

# Function to calculate the modular inverse using Extended Euclidean Algorithm
def modular_inverse(a, m):
    m0, x0, x1 = m, 0, 1
    while a > 1:
        q = a // m
        a, m = m, a % m
        x0, x1 = x1 - q * x0, x0
    if x1 < 0:
        x1 += m0
    return x1

# Lehmer's GCD Algorithm
def lehmers_gcd(a, b):
    while b != 0:
        if b < 10**4:
            return gcd(a, b)
        a1, b1 = divmod(a, 10**(len(str(b)) // 2))
        a2, b2 = divmod(b, 10**(len(str(b)) // 2))
        if a1 == 0 or b1 == 0:
            return gcd(a, b)
        q = a1 // b1
        a -= q * b
        a, b = b, a
    return a

# Caesar Cipher Algorithm
def caesar_cipher(text, shift, mode='encrypt'):
    if mode == 'decrypt':
        shift = -shift
    result = ''.join(
        chr((ord(char) - 65 + shift) % 26 + 65) if char.isupper() else
        chr((ord(char) - 97 + shift) % 26 + 97) if char.islower() else char
        for char in text
    )
    return result

# DES Encryption/Decryption
def des_encrypt_decrypt(text, key, mode='encrypt'):
    cipher = DES.new(key, DES.MODE_ECB)
    if mode == 'encrypt':
        encrypted = cipher.encrypt(pad(text.encode(), DES.block_size))
        return encrypted.hex()
    elif mode == 'decrypt':
        decrypted = unpad(cipher.decrypt(bytes.fromhex(text)), DES.block_size)
        return decrypted.decode()

# Menu-driven program
def menu():
    while True:
        print("\nMenu:")
        print("1. Check if a number is prime")
        print("2. Calculate modular inverse")
        print("3. Lehmer's GCD Algorithm")
        print("4. Caesar Cipher")
        print("5. DES Encryption/Decryption")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            num = int(input("Enter a number to check if it's prime: "))
            print(f"{num} is {'a prime number' if is_prime(num) else 'not a prime number'}.")

        elif choice == '2':
            a = int(input("Enter the number (a): "))
            m = int(input("Enter the modulus (m): "))
            try:
                inv = modular_inverse(a, m)
                print(f"The modular inverse of {a} modulo {m} is: {inv}")
            except ValueError:
                print("Modular inverse does not exist.")

        elif choice == '3':
            a = int(input("Enter the first number (a): "))
            b = int(input("Enter the second number (b): "))
            gcd_result = lehmers_gcd(a, b)
            print(f"Lehmer's GCD of {a} and {b} is: {gcd_result}")

        elif choice == '4':
            text = input("Enter the text: ")
            shift = int(input("Enter the shift value: "))
            mode = input("Choose mode (encrypt/decrypt): ").strip().lower()
            if mode not in ['encrypt', 'decrypt']:
                print("Invalid mode. Please choose 'encrypt' or 'decrypt'.")
                continue
            result = caesar_cipher(text, shift, mode)
            print(f"Result: {result}")

        elif choice == '5':
            text = input("Enter text: ")
            key = input("Enter 8-byte key: ").encode()
            if len(key) != 8:
                print("Key must be exactly 8 bytes!")
                continue
            mode = input("Choose mode (encrypt/decrypt): ").strip().lower()
            if mode == 'encrypt':
                encrypted = des_encrypt_decrypt(text, key, mode)
                print(f"Encrypted text (hex): {encrypted}")
            elif mode == 'decrypt':
                decrypted = des_encrypt_decrypt(text, key, mode)
                print(f"Decrypted text: {decrypted}")
            else:
                print("Invalid mode. Please choose 'encrypt' or 'decrypt'.")

        elif choice == '6':
            print("Exiting the program.")
            break

        else:
            print("Invalid choice. Please try again.")

# Run the menu
if __name__ == "__main__":
    menu()
