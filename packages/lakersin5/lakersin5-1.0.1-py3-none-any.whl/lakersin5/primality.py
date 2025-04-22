import random

def is_prime_miller_rabin(n, k=5):  
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2

    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)  
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True


def is_prime_solovay_strassen(n, k=5):  
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False

    def jacobi_symbol(a, n):
        if n <= 0 or n % 2 == 0:
            raise ValueError("n must be a positive odd number.")
        result = 1
        if a < 0:
            a = -a
            if n % 4 == 3:
                result = -result
        while a != 0:
            while a % 2 == 0:
                a //= 2
                if n % 8 in [3, 5]:
                    result = -result
            a, n = n, a  
            if a % 4 == 3 and n % 4 == 3:
                result = -result
            a %= n
        return result if n == 1 else 0

    for _ in range(k):
        a = random.randint(2, n - 2)
        x = jacobi_symbol(a, n)
        if x == 0 or pow(a, (n - 1) // 2, n) != (x % n):
            return False
    return True


def menu():
    while True:
        print("\nPrimality Testing")
        print("A. Miller-Rabin Test")
        print("B. Solovay-Strassen Test")
        print("C. Exit")
        choice = input("Choose an option (A/B/C): ").strip().upper()

        if choice == 'A':
            n = int(input("Enter the number: "))
            k = int(input("Enter iterations: "))
            if is_prime_miller_rabin(n, k):
                print(f"{n} is probably prime (Miller-Rabin Test).")
            else:
                print(f"{n} is not prime (Miller-Rabin Test).")

        elif choice == 'B':
            n = int(input("Enter the number to test for primality: "))
            k = int(input("Enter the number of iterations: "))
            if is_prime_solovay_strassen(n, k):
                print(f"{n} is probably prime (Solovay-Strassen Test).")
            else:
                print(f"{n} is not prime (Solovay-Strassen Test).")

        elif choice == 'C':
            print("Exiting the program.")
            break

        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    menu()
