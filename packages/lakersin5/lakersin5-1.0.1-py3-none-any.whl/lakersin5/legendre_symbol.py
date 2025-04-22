# lakersin5/legendre_jacobi.py

def legendre_symbol(a, p):
    return pow(a, (p - 1) // 2, p)

def jacobi_symbol(a, n):
    if n % 2 == 0:
        raise ValueError("Jacobi symbol is only defined for odd integers.")
    result = 1
    a = a % n
    while a != 0:
        while a % 2 == 0:
            a //= 2
            if n % 8 in [3, 5]:
                result = -result
        a, n = n, a  # reciprocity
        if a % 4 == 3 and n % 4 == 3:
            result = -result
        a = a % n
    return result if n == 1 else 0

def run_legendre_jacobi_demo():
    print("\n=== Legendre & Jacobi Symbol Demo ===")

    a = 5
    p = 11
    print(f"Legendre({a}/{p}) = {legendre_symbol(a, p)}")

    a = 1001
    n = 9907
    print(f"Jacobi({a}/{n}) = {jacobi_symbol(a, n)}")

if __name__ == "__main__":
    run_legendre_jacobi_demo()