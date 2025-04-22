# lakersin5/ecc_signature.py
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
import hashlib

def modinv(a, m):
    return pow(a, -1, m)

def hash_message(msg):
    return int(hashlib.sha256(msg.encode()).hexdigest(), 16)

def sign(curve, private_key, msg):
    e = hash_message(msg)
    k = 5  # In real-world, use random k
    R = k * curve.G
    r = R.x % curve.n
    s = (modinv(k, curve.n) * (e + private_key * r)) % curve.n
    return (r, s)

def verify(curve, public_key, msg, signature):
    r, s = signature
    e = hash_message(msg)
    w = modinv(s, curve.n)
    u1 = (e * w) % curve.n
    u2 = (r * w) % curve.n
    P = u1 * curve.G + u2 * public_key
    return r == P.x % curve.n

def run_ecc_signature_demo():
    print("\n=== ECC Digital Signature Demo ===")
    p = 211
    a = 0
    b = -4
    G = Point(2, 2, None)
    curve = EllipticCurve(a, b, p, G, n=199)
    G.curve = curve

    private_key = 121
    public_key = private_key * curve.G

    msg = "Hello ECC"

    signature = sign(curve, private_key, msg)
    print(f"Message: {msg}")
    print(f"Signature: {signature}")
    print("Valid Signature?" , verify(curve, public_key, msg, signature))

if __name__ == "__main__":
    run_ecc_signature_demo()