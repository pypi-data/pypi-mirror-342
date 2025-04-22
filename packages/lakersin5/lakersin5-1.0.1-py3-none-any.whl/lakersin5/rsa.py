import random
from sympy import isprime, mod_inverse

# Function to generate prime numbers
def generate_prime(bits=8):
    while True:
        num = random.getrandbits(bits)
        if isprime(num):
            return num

# RSA Key Generation
def rsa_keygen():
    p = generate_prime()
    q = generate_prime()
    n = p * q
    phi = (p - 1) * (q - 1)

    # Choose e such that 1 < e < phi(n) and gcd(e, phi) = 1
    e = random.choice([3, 5, 17, 257, 65537])
    while phi % e == 0:
        e = random.choice([3, 5, 17, 257, 65537])

    d = mod_inverse(e, phi)  # Compute modular inverse
    return (e, n), (d, n), p, q

# RSA Encryption
def rsa_encrypt(plaintext, pub_key):
    e, n = pub_key
    cipher = [pow(ord(char), e, n) for char in plaintext]
    return cipher

# RSA Decryption
def rsa_decrypt(ciphertext, priv_key):
    d, n = priv_key
    plain = "".join(chr(pow(char, d, n)) for char in ciphertext)
    return plain

# Jacobi Symbol Calculation
def jacobi_symbol(a, n):
    if n <= 0 or n % 2 == 0:
        return 0  # Invalid input

    j = 1
    while a != 0:
        while a % 2 == 0:
            a //= 2
            if n % 8 in [3, 5]:
                j = -j

        a, n = n, a  # Reciprocity
        if a % 4 == n % 4 == 3:
            j = -j
        a %= n

    return j if n == 1 else 0

# Main menu-driven program
if __name__ == "__main__":
    while True:
        print("\n===== MENU =====")
        print("1. RSA Key Generation")
        print("2. RSA Encryption")
        print("3. RSA Decryption")
        print("4. Jacobi Symbol Calculation")
        print("5. Exit")
        
        choice = input("Enter your choice: ")

        if choice == "1":
            pub_key, priv_key, p, q = rsa_keygen()
            print(f"🔑 Public Key (e, n): {pub_key}")
            print(f"🔐 Private Key (d, n): {priv_key}")
            print(f"Prime Numbers: p={p}, q={q}")

        elif choice == "2":
            plaintext = input("Enter text to encrypt: ")
            e = int(input("Enter public exponent (e): "))
            n = int(input("Enter modulus (n): "))
            cipher = rsa_encrypt(plaintext, (e, n))
            print(f"🔐 Encrypted Text: {cipher}")

        elif choice == "3":
            ciphertext = list(map(int, input("Enter encrypted numbers (comma-separated): ").split(',')))
            d = int(input("Enter private exponent (d): "))
            n = int(input("Enter modulus (n): "))
            decrypted_text = rsa_decrypt(ciphertext, (d, n))
            print(f"🔓 Decrypted Text: {decrypted_text}")

        elif choice == "4":
            a = int(input("Enter value of a: "))
            n = int(input("Enter value of n: "))
            print(f"✅ Jacobi Symbol ({a}/{n}) = {jacobi_symbol(a, n)}")

        elif choice == "5":
            print("Exiting program... 👋")
            break

        else:
            print("❌ Invalid choice! Please select a valid option.")
