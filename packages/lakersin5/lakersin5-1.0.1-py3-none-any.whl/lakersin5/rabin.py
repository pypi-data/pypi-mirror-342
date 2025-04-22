import random

def is_prime(n):
    """Check if a number is prime."""
    if n < 2:
        return False
    for i in range(2, int(n ** 0.5) + 1):
        if n % i == 0:
            return False
    return True

def extended_euclidean(a, b):
    """Finds z_p and z_q such that z_p * p + z_q * q = 1."""
    x0, x1, y0, y1 = 1, 0, 0, 1
    while b:
        q, a, b = a // b, b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1
    return x0, y0

def encrypt(message, n):
    """Encrypt a numeric message using the Rabin cryptosystem."""
    m = int(message)  # Convert input to integer
    if m >= n:
        raise ValueError("Message must be smaller than n.")
    
    c = (m ** 2) % n  # Compute ciphertext
    return c

def decrypt(c, p, q):
    """Decrypt a ciphertext using the Rabin cryptosystem."""
    n = p * q

    # Compute square roots mod p and q
    mp = pow(c, (p + 1) // 4, p)
    mq = pow(c, (q + 1) // 4, q)

    # Compute coefficients using Extended Euclidean Algorithm
    zp, zq = extended_euclidean(p, q)

    # Compute the four possible plaintexts
    r1 = (zp * p * mq + zq * q * mp) % n
    r2 = n - r1
    r3 = (zp * p * mq - zq * q * mp) % n
    r4 = n - r3

    # Return four possible numeric messages
    return {r1, r2, r3, r4}

# Main Execution
if __name__ == "__main__":
    # User inputs primes p and q
    while True:
        try:
            p = int(input("Enter a prime number p (must be 3 mod 4): "))
            q = int(input("Enter a prime number q (must be 3 mod 4): "))

            # Validate primes
            if not (is_prime(p) and is_prime(q)):
                print("Both numbers must be prime.")
                continue
            if p % 4 != 3 or q % 4 != 3:
                print("Both numbers must be congruent to 3 mod 4.")
                continue
            break
        except ValueError:
            print("Invalid input. Please enter valid prime numbers.")

    # Compute public key n
    n = p * q
    print("\nPublic Key (n):", n)

    # Encrypt a message
    message = input("Enter a numeric message to encrypt: ")
    try:
        ciphertext = encrypt(message, n)
        print("Ciphertext:", ciphertext)
    except ValueError as e:
        print("Encryption Error:", e)
        exit()

    # Decrypt the ciphertext
    decrypted_messages = decrypt(ciphertext, p, q)
    print("Possible decrypted messages:", decrypted_messages)
