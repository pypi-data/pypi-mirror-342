# Function to compute modular exponentiation (a^b mod m)
def mod_exp(a, b, m):
    return pow(a, b, m)

# Function to compute modular inverse using Extended Euclidean Algorithm
def mod_inverse(e, phi_n):
    g, x, _ = extended_gcd(e, phi_n)
    if g != 1:
        raise ValueError("No modular inverse exists for the given e and φ(n).")
    return x % phi_n

# Extended Euclidean Algorithm to compute gcd and modular inverse
def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    g, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return g, x, y

# RSA Encryption & Decryption
def rsa_encrypt(m, e, n):
    return mod_exp(m, e, n)  # C = m^e mod n

def rsa_decrypt(c, d, n):
    return mod_exp(c, d, n)  # m = C^d mod n

# User Inputs
p = int(input("Enter prime number p: "))
q = int(input("Enter prime number q: "))
e = int(input("Enter public exponent e: "))

# Compute RSA Parameters
n = p * q
phi_n = (p - 1) * (q - 1)

# Compute private exponent d
d = mod_inverse(e, phi_n)

print(f"\n🔹 Calculated Values 🔹")
print(f"n = p * q = {n}")
print(f"φ(n) = (p-1) * (q-1) = {phi_n}")
print(f"Private exponent d = {d}")

# User Input for Messages
m1 = int(input("\nEnter first plaintext message m1: "))
m2 = int(input("Enter second plaintext message m2: "))

# Encrypt messages
C1 = rsa_encrypt(m1, e, n)
C2 = rsa_encrypt(m2, e, n)

print(f"\n🔹 Encryption 🔹")
print(f"C1 = Enc(m1) = {C1}")
print(f"C2 = Enc(m2) = {C2}")

# Homomorphic Multiplication: C12 = C1 * C2 mod n
C12 = (C1 * C2) % n

print(f"\n🔹 Homomorphic Multiplication 🔹")
print(f"C12 = (C1 * C2) mod n = {C12}")

# Decrypt the result
decrypted_product = rsa_decrypt(C12, d, n)

print(f"\n🔹 Decryption 🔹")
print(f"Decrypted Product = {decrypted_product}")

# Verification
expected_product = (m1 * m2) % n
print(f"Expected Product (m1 * m2) mod n = {expected_product}")
assert decrypted_product == expected_product, "Decryption failed!"
print("\n✅ RSA Homomorphic Encryption verified successfully!")
