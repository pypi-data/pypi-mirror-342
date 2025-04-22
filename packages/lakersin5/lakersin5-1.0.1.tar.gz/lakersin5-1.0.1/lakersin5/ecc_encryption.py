# lakersin5/ecc_encryption.py

class Point:
    def __init__(self, x, y, curve):
        self.x = x
        self.y = y
        self.curve = curve

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.curve == other.curve

    def __neg__(self):
        return Point(self.x, -self.y % self.curve.p, self.curve)

    def __add__(self, other):
        if self == other:
            return self.double()
        return self.curve.add_points(self, other)

    def double(self):
        return self.curve.double_point(self)

    def __rmul__(self, scalar):
        return self.curve.scalar_mult(scalar, self)


class EllipticCurve:
    def __init__(self, a, b, p, G, n):
        self.a = a
        self.b = b
        self.p = p
        self.G = G
        self.n = n

    def is_on_curve(self, P):
        if P is None:
            return True
        return (P.y ** 2 - (P.x ** 3 + self.a * P.x + self.b)) % self.p == 0

    def add_points(self, P, Q):
        if P is None: return Q
        if Q is None: return P
        if P.x == Q.x and (P.y + Q.y) % self.p == 0:
            return None

        if P == Q:
            return self.double_point(P)

        m = ((Q.y - P.y) * pow(Q.x - P.x, -1, self.p)) % self.p
        x_r = (m ** 2 - P.x - Q.x) % self.p
        y_r = (m * (P.x - x_r) - P.y) % self.p
        return Point(x_r, y_r, self)

    def double_point(self, P):
        if P is None: return None

        m = ((3 * P.x ** 2 + self.a) * pow(2 * P.y, -1, self.p)) % self.p
        x_r = (m ** 2 - 2 * P.x) % self.p
        y_r = (m * (P.x - x_r) - P.y) % self.p
        return Point(x_r, y_r, self)

    def scalar_mult(self, k, P):
        result = None
        addend = P

        while k:
            if k & 1:
                result = self.add_points(result, addend)
            addend = self.double_point(addend)
            k >>= 1

        return result


def encrypt(curve, public_key, plaintext_point):
    k = 7  # In real-world usage, use random.randint(1, curve.n-1)
    C1 = k * curve.G
    C2 = plaintext_point + k * public_key
    return C1, C2


def decrypt(curve, private_key, C1, C2):
    shared_secret = private_key * C1
    return C2 + (-shared_secret)


def run_ecc_encryption_demo():
    print("\n=== ECC Encryption Demo ===")

    # Define curve and keys
    p = 211
    a = 0
    b = -4
    G = Point(2, 2, None)
    curve = EllipticCurve(a, b, p, G, n=199)
    G.curve = curve

    private_key = 121
    public_key = private_key * curve.G

    # Define plaintext point
    plaintext_point = 3 * curve.G
    print(f"Plaintext Point: ({plaintext_point.x}, {plaintext_point.y})")

    # Encrypt
    C1, C2 = encrypt(curve, public_key, plaintext_point)
    print(f"Ciphertext C1: ({C1.x}, {C1.y})")
    print(f"Ciphertext C2: ({C2.x}, {C2.y})")

    # Decrypt
    decrypted = decrypt(curve, private_key, C1, C2)
    print(f"Decrypted Point: ({decrypted.x}, {decrypted.y})")

if __name__ == "__main__":
    run_ecc_encryption_demo()