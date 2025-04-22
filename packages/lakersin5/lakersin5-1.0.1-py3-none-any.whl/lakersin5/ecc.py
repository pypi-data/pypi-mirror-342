def mod_inverse(a, p):
    """Computes modular inverse using Extended Euclidean Algorithm."""
    g, x, y = extended_gcd(a, p)
    if g != 1:
        raise ValueError(f"No modular inverse exists for {a} mod {p}")
    return x % p  # Ensure positive result

def extended_gcd(a, b):
    """Extended Euclidean Algorithm to find GCD and coefficients x, y such that ax + by = gcd(a, b)."""
    if a == 0:
        return b, 0, 1
    g, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return g, x, y

def point_doubling(xp, yp, a, p):
    """Computes 2P = P + P using the doubling formula."""
    if yp == 0:
        return None  # Point at infinity

    num = (3 * xp**2 + a) % p
    denom = (2 * yp) % p
    try:
        lam = (num * mod_inverse(denom, p)) % p
    except ValueError:
        return None  # Point at infinity

    xr = (lam**2 - 2 * xp) % p
    yr = (lam * (xp - xr) - yp) % p

    return (xr, yr)

def point_addition(xp, yp, xq, yq, p):
    """Computes P + Q using elliptic curve addition formula."""
    if (xp, yp) == (xq, yq):  
        return point_doubling(xp, yp, a, p)

    if xp == xq:  
        return None  # Points are vertical, result is point at infinity

    num = (yq - yp) % p
    denom = (xq - xp) % p
    try:
        lam = (num * mod_inverse(denom, p)) % p
    except ValueError:
        return None  # Point at infinity

    xr = (lam**2 - xp - xq) % p
    yr = (lam * (xp - xr) - yp) % p

    return (xr, yr)

def point_multiplication(P, k, a, p):
    """Computes k * P using repeated **point doubling only**."""
    Q = P  
    for _ in range(k - 1):  
        Q = point_doubling(Q[0], Q[1], a, p)  
    return Q

if __name__ == "__main__":
    # User input for elliptic curve parameters
    a = int(input("Enter coefficient a: "))
    b = int(input("Enter coefficient b: "))
    p = int(input("Enter prime modulus p: "))

    # User input for generator point G
    gx = int(input("Enter x-coordinate of G: ")) % p
    gy = int(input("Enter y-coordinate of G: ")) % p
    G = (gx, gy)

    # User input for plaintext message point P
    px = int(input("Enter x-coordinate of P (Message Point): ")) % p
    py = int(input("Enter y-coordinate of P (Message Point): ")) % p
    P = (px, py)

    # User input for private keys
    PriA = int(input("Enter private key PriA: "))
    PriB = int(input("Enter private key PriB: "))

    # Compute public keys using repeated **point doubling**
    PubA = point_multiplication(G, PriA, a, p)
    PubB = point_multiplication(G, PriB, a, p)

    print(f"Public Key PubA: {PubA}")
    print(f"Public Key PubB: {PubB}")

    # User input for encryption random k
    k = int(input("Enter random value k for encryption: "))

    # Encryption: Compute C1 using repeated **point doubling**
    C1 = point_multiplication(G, k, a, p)  # C1 = kG

    # Compute PriB * G using repeated **point doubling**
    PriB_G = point_multiplication(G, PriB, a, p)  # PriB * G
    PriA_PriB_G = point_multiplication(PriB_G, PriA, a, p)  # PriA * (PriB * G)

    # Compute C2 = P + PriA * (PriB * G) using **point addition**
    C2 = point_addition(P[0], P[1], PriA_PriB_G[0], PriA_PriB_G[1], p)

    print(f"Ciphertext C1: {C1}")
    print(f"Ciphertext C2: {C2}")

    # Decryption: Compute original P
    d = int(input("Enter decryption key d: "))  # Receiver's private key

    # Compute S' = d * C1 using **point doubling**
    S_prime = point_multiplication(C1, d, a, p)

    # Negate S'
    S_prime_neg = (S_prime[0], (-S_prime[1]) % p)

    # Compute decrypted plaintext P = C2 - S' using **point addition**
    decrypted_P = point_addition(C2[0], C2[1], S_prime_neg[0], S_prime_neg[1], p)

    print(f"Decrypted Message Point P: {decrypted_P}")
