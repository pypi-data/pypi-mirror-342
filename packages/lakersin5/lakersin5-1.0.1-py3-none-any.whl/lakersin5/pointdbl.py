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

    # Compute slope λ = (3 * xp^2 + a) / (2 * yp) mod p
    num = (3 * xp**2 + a) % p
    denom = (2 * yp) % p
    try:
        lam = (num * mod_inverse(denom, p)) % p
    except ValueError:
        return None  # Point at infinity

    # Compute new x and y coordinates
    xr = (lam**2 - 2 * xp) % p
    yr = (lam * (xp - xr) - yp) % p

    return (xr, yr)

def compute_ZP_by_doubling(P, Z, a, p):
    """Computes ZP using sequential doubling."""
    Q = P  # Start with P
    for i in range(2, Z + 1):
        Q = point_doubling(Q[0], Q[1], a, p)  # Compute (i)P as 2 * (i-1)P
        if Q is None:
            print(f"{i}P is the point at infinity")
            return None
        print(f"{i}P = {Q}")  # Print each doubling step
    
    return Q


if __name__ == "__main__":
    # User input for elliptic curve parameters
    a = int(input("Enter coefficient a: "))
    b = int(input("Enter coefficient b: "))
    p = int(input("Enter prime modulus p: "))

    # User input for point P
    xp = int(input("Enter x-coordinate of P: ")) % p
    yp = int(input("Enter y-coordinate of P: ")) % p

    # User input for multiplication factor Z
    Z = int(input("Enter the multiplication factor Z: "))

    # Perform point doubling sequentially
    P = (xp, yp)
    result = compute_ZP_by_doubling(P, Z, a, p)

    if result:
        print(f"{Z}P = {result}")
    else:
        print(f"{Z}P is the point at infinity (identity element).")
