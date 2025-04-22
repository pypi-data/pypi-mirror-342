import math

def lcm(x, y):
    """Compute the least common multiple of x and y."""
    return (x * y) // math.gcd(x, y)

def L(x, n):
    """L function: L(x) = (x - 1) / n"""
    return (x - 1) // n

# 🔹 Step 1: Key Generation
p = int(input("Enter prime number p: "))
q = int(input("Enter prime number q: "))

n = p * q
lambda_ = lcm(p - 1, q - 1)
g = n + 1  # Standard choice for Paillier encryption

# Compute mu
mu = pow(g, lambda_, n**2)  # g^lambda mod n^2
L_mu = L(mu, n)  # L(mu)

print(f"\n🔹 Public Key (n, g) = ({n}, {g})")
print(f"🔹 Private Key (λ, L(μ)) = ({lambda_}, {L_mu})")

# 🔹 Step 2: Encryption
m1 = int(input("\nEnter first plaintext message m1: "))
m2 = int(input("Enter second plaintext message m2: "))
r1 = int(input("Enter random number r1 for m1 encryption: "))
r2 = int(input("Enter random number r2 for m2 encryption: "))

# Encrypt messages
C1 = (pow(g, m1, n**2) * pow(r1, n, n**2)) % n**2
C2 = (pow(g, m2, n**2) * pow(r2, n, n**2)) % n**2

print("\n🔹 Encrypted Messages:")
print(f"C1 = Enc(m1) = {C1}")
print(f"C2 = Enc(m2) = {C2}")

# 🔹 Step 3: Homomorphic Addition
C12 = (C1 * C2) % n**2
print(f"\n🔹 Homomorphic Addition Result:\nC12 = (C1 * C2) mod n^2 = {C12}")

# 🔹 Step 4: Decryption
u = pow(C12, lambda_, n**2)  # Compute u = C12^lambda mod n^2
L_u = L(u, n)  # Compute L(u)
decrypted_sum = (L_u * L_mu) % n  # Compute decrypted plaintext

print("\n🔹 Decryption:")
print(f"Decrypted Sum = {decrypted_sum}")
print(f"Expected Sum (m1 + m2 mod n) = {(m1 + m2) % n}")

# ✅ Verification
if decrypted_sum == (m1 + m2) % n:
    print("\n✅ Paillier Homomorphic Encryption verified successfully!")
else:
    print("\n❌ Error: Decrypted value does not match expected sum.")
