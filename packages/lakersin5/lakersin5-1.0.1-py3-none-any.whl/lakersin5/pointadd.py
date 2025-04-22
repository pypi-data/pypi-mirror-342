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

def point_addition(xp, yp, xq, yq, p):
    """Computes P + Q using elliptic curve addition formula."""
    if (xp, yp) == (xq, yq):  
        return None  # This is point doubling, use separate function

    if xp == xq:  
        return None  # Points are vertical, result is point at infinity

    # Compute slope λ = (yq - yp) / (xq - xp) mod p
    num = (yq - yp) % p
    denom = (xq - xp) % p
    try:
        lam = (num * mod_inverse(denom, p)) % p
    except ValueError:
        return None  # Point at infinity

    # Compute new x and y coordinates
    xr = (lam**2 - xp - xq) % p
    yr = (lam * (xp - xr) - yp) % p

    return (xr, yr)

if __name__ == "__main__":
    # User input for elliptic curve parameters
    p = int(input("Enter prime modulus p: "))

    # User input for point P
    xp = int(input("Enter x-coordinate of P: ")) % p
    yp = int(input("Enter y-coordinate of P: ")) % p

    # User input for point Q
    xq = int(input("Enter x-coordinate of Q: ")) % p
    yq = int(input("Enter y-coordinate of Q: ")) % p

    # Perform point addition
    result = point_addition(xp, yp, xq, yq, p)

    if result:
        print(f"P + Q = {result}")
    else:
        print("P + Q is the point at infinity (identity element).")
