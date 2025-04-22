import sympy
import random

# Step 1: Key Generation (User Input)
def generate_keys():
    # User inputs prime number p
    p = int(input("Enter a prime number (p): "))
    if not sympy.isprime(p):
        raise ValueError("p must be a prime number!")

    # User inputs generator g
    g = int(input(f"Enter a generator (g) such that 1 < g < {p}: "))
    if not (1 < g < p):
        raise ValueError("g must be between 1 and p-1.")

    # User inputs private key x
    x = int(input(f"Enter a private key (x) such that 1 < x < {p-1}: "))
    if not (1 < x < p - 1):
        raise ValueError("x must be between 1 and p-2.")

    # Compute public key component y = g^x mod p
    y = pow(g, x, p)

    public_key = (p, g, y)
    private_key = x
    return public_key, private_key

# Step 2: Signing a Message
def sign_message(message, private_key, public_key):
    p, g, y = public_key
    x = private_key

    while True:
        k = int(input(f"Enter a random k such that 1 < k < {p-1} and gcd(k, {p-1}) = 1: "))
        if 1 < k < p - 1 and sympy.gcd(k, p - 1) == 1:
            break
        print("Invalid k! Choose another value.")

    r = pow(g, k, p)  # r = g^k mod p
    k_inv = pow(k, -1, p - 1)  # Compute modular inverse of k mod (p-1)
    s = (k_inv * (message - x * r)) % (p - 1)  # s = k⁻¹ * (m - x*r) mod (p-1)

    return (r, s)

# Step 3: Verifying the Signature
def verify_signature(message, signature, public_key):
    p, g, y = public_key
    r, s = signature

    if not (1 <= r < p):
        return False  # r must be in range [1, p-1]

    # Verification equations:
    v1 = (pow(y, r, p) * pow(r, s, p)) % p  # y^r * r^s mod p
    v2 = pow(g, message, p)  # g^m mod p

    return v1 == v2  # Signature is valid if v1 == v2

# Main Execution
if __name__ == "__main__":
    try:
        # User inputs keys
        public_key, private_key = generate_keys()
        print(f"Public Key: {public_key}")
        print(f"Private Key: {private_key}")

        # User inputs the message
        message = int(input("Enter a numeric message to sign: "))

        # Signing the message
        signature = sign_message(message, private_key, public_key)
        print(f"Signature: {signature}")

        # Verifying the signature
        is_valid = verify_signature(message, signature, public_key)
        print("Signature is VALID ✅" if is_valid else "Signature is INVALID ❌")

    except ValueError as e:
        print(f"Error: {e}")
