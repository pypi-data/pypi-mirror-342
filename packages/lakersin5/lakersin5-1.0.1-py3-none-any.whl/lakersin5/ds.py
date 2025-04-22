import sympy

# Step 1: Key Generation
def generate_keys(p, q):
    if not (sympy.isprime(p) and sympy.isprime(q)):
        raise ValueError("Both numbers must be prime!")
    
    n = p * q  # Compute modulus
    phi = (p - 1) * (q - 1)  # Compute Euler's totient function

    e = 17  # Public exponent (commonly chosen)
    if sympy.gcd(e, phi) != 1:
        e = sympy.nextprime(e)  # Ensure e is coprime with phi(n)
    
    d = pow(e, -1, phi)  # Compute modular inverse of e modulo phi

    return (e, n), (d, n)  # (Public Key), (Private Key)

# Step 2: Signing a message
def sign_message(message, private_key):
    d, n = private_key
    signature = pow(message, d, n)  # S = M^d mod n (Modular exponentiation)
    return signature

# Step 3: Verifying the signature
def verify_signature(signature, public_key):
    e, n = public_key
    decrypted_message = pow(signature, e, n)  # H'(M) = S^e mod n
    return decrypted_message  # Returns the recovered message

# Main execution
if __name__ == "__main__":
    try:
        # User inputs prime numbers
        p = int(input("Enter a prime number (p): "))
        q = int(input("Enter another prime number (q): "))
        
        public_key, private_key = generate_keys(p, q)

        # User input for the message
        message = int(input(f"Enter a number as a message to sign (1-{public_key[1]-1}): "))
        if not (1 <= message < public_key[1]):
            print("Invalid message! Choose a number between 1 and n-1.")
        else:
            # Signing the message
            signature = sign_message(message, private_key)
            print(f"Signature: {signature}")

            # Verifying the signature
            recovered_message = verify_signature(signature, public_key)
            print(f"Recovered Message: {recovered_message}")

            # Check if the signature is valid
            if recovered_message == message:
                print("Signature is VALID ✅")
            else:
                print("Signature is INVALID ❌")

    except ValueError as e:
        print(f"Error: {e}")
