# ======== ECC and ECDSA Utility Functions ========

def mod_inverse(a, p):
    g, x, y = extended_gcd(a, p)
    if g != 1:
        raise ValueError(f"No modular inverse for {a} mod {p}")
    return x % p

def extended_gcd(a, b):
    if a == 0:
        return b, 0, 1
    g, x1, y1 = extended_gcd(b % a, a)
    x = y1 - (b // a) * x1
    y = x1
    return g, x, y

def point_doubling(xp, yp, a, p):
    if yp == 0:
        return None
    num = (3 * xp**2 + a) % p
    denom = (2 * yp) % p
    lam = (num * mod_inverse(denom, p)) % p
    xr = (lam**2 - 2 * xp) % p
    yr = (lam * (xp - xr) - yp) % p
    return (xr, yr)

def point_addition(xp, yp, xq, yq, p):
    if (xp, yp) == (xq, yq):
        return point_doubling(xp, yp, a, p)
    if xp == xq:
        return None
    num = (yq - yp) % p
    denom = (xq - xp) % p
    lam = (num * mod_inverse(denom, p)) % p
    xr = (lam**2 - xp - xq) % p
    yr = (lam * (xp - xr) - yp) % p
    return (xr, yr)

def point_multiplication(P, k, a, p):
    Q = P
    for _ in range(k - 1):
        Q = point_doubling(Q[0], Q[1], a, p)
        if Q is None:
            return (None, None)
    return Q

# ======== Signature Generation with Steps ========

def generate_signature(z, d, G, a, p, n, k):
    print("\n=== Signature Generation Steps ===")
    
    R = point_multiplication(G, k, a, p)
    print(f"Step 1: R = k * G = {k} * {G} = {R}")
    
    r = R[0] % n
    print(f"Step 2: r = R.x mod n = {R[0]} mod {n} = {r}")
    if r == 0:
        raise ValueError("r = 0, choose another k")
    
    k_inv = mod_inverse(k, n)
    print(f"Step 3: k⁻¹ mod n = {k}⁻¹ mod {n} = {k_inv}")
    
    s = (k_inv * (z + r * d)) % n
    print(f"Step 4: s = k⁻¹ * (z + r * d) mod n = {k_inv} * ({z} + {r} * {d}) mod {n} = {s}")
    
    if s == 0:
        raise ValueError("s = 0, choose another k")
    
    print(f"Signature (r, s): ({r}, {s})")
    print("=== Signature Generation Complete ===\n")
    return r, s

# ======== Signature Verification with Steps ========

def verify_signature(z, r, s, G, Q, a, p, n):
    print("\n=== Signature Verification Steps ===")

    print(f"Step 1: Compute w = s⁻¹ mod n = {s}⁻¹ mod {n}")
    try:
        w = mod_inverse(s, n)
    except ValueError as e:
        print(f"   ❌ Error: {e}")
        return False
    print(f"       → w = {w}")

    u1 = (z * w) % n
    print(f"Step 2: Compute u1 = z * w mod n = {z} * {w} mod {n} = {u1}")

    u2 = (r * w) % n
    print(f"Step 3: Compute u2 = r * w mod n = {r} * {w} mod {n} = {u2}")

    print(f"Step 4: Compute U1 = u1 * G = {u1} * {G}")
    U1 = point_multiplication(G, u1, a, p)
    print(f"       → U1 = {U1}")

    print(f"Step 5: Compute U2 = u2 * Q = {u2} * {Q}")
    U2 = point_multiplication(Q, u2, a, p)
    print(f"       → U2 = {U2}")

    print(f"Step 6: Compute R = U1 + U2 = {U1} + {U2}")
    R = point_addition(U1[0], U1[1], U2[0], U2[1], p)
    print(f"       → R = {R}")

    if R is None:
        print("   ❌ R is point at infinity → Signature Invalid")
        return False

    print(f"Step 7: Check if R.x mod n == r → {R[0]} mod {n} == {r}")
    valid = (R[0] % n) == r
    print("       →", "✅ Signature Valid" if valid else "❌ Signature Invalid")
    print("=== Signature Verification Complete ===\n")
    return valid

# ======== MAIN Program ========

if __name__ == "__main__":
    a = int(input("Enter coefficient a: "))
    b = int(input("Enter coefficient b: "))
    p = int(input("Enter prime modulus p: "))
    n = int(input("Enter order of base point n: "))

    gx = int(input("Enter x-coordinate of G: ")) % p
    gy = int(input("Enter y-coordinate of G: ")) % p
    G = (gx, gy)

    px = int(input("Enter x-coordinate of P (Message): ")) % p
    py = int(input("Enter y-coordinate of P (Message): ")) % p
    P = (px, py)

    PriA = int(input("Enter private key PriA: "))
    PriB = int(input("Enter private key PriB: "))

    PubA = point_multiplication(G, PriA, a, p)
    PubB = point_multiplication(G, PriB, a, p)
    print(f"Public Key A: {PubA}")
    print(f"Public Key B: {PubB}")

    k = int(input("Enter random value k for encryption: "))
    C1 = point_multiplication(G, k, a, p)
    PriB_G = point_multiplication(G, PriB, a, p)
    PriA_PriB_G = point_multiplication(PriB_G, PriA, a, p)
    C2 = point_addition(P[0], P[1], PriA_PriB_G[0], PriA_PriB_G[1], p)
    print(f"Ciphertext C1: {C1}")
    print(f"Ciphertext C2: {C2}")

    d = int(input("Enter decryption key d (usually receiver's private key): "))
    S = point_multiplication(C1, d, a, p)
    S_neg = (S[0], (-S[1]) % p)
    decrypted_P = point_addition(C2[0], C2[1], S_neg[0], S_neg[1], p)
    print(f"Decrypted Message Point: {decrypted_P}")

    z = int(input("Enter hashed message (z): "))
    ds_k = int(input("Enter random k for signature (1 < k < n): "))
    r, s = generate_signature(z, d, G, a, p, n, ds_k)
    print(f"Signature (r, s): ({r}, {s})")

    Q = point_multiplication(G, d, a, p)
    is_valid = verify_signature(z, r, s, G, Q, a, p, n)
    print("Signature Verification:", "✅ Valid" if is_valid else "❌ Invalid")
