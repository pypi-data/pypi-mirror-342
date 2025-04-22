# lakersin5/full_des.py

# Initial Permutation
IP = [58, 50, 42, 34, 26, 18, 10, 2,
      60, 52, 44, 36, 28, 20, 12, 4,
      62, 54, 46, 38, 30, 22, 14, 6,
      64, 56, 48, 40, 32, 24, 16, 8,
      57, 49, 41, 33, 25, 17, 9, 1,
      59, 51, 43, 35, 27, 19, 11, 3,
      61, 53, 45, 37, 29, 21, 13, 5,
      63, 55, 47, 39, 31, 23, 15, 7]

# Final Permutation (inverse of IP)
IP_INV = [40, 8, 48, 16, 56, 24, 64, 32,
          39, 7, 47, 15, 55, 23, 63, 31,
          38, 6, 46, 14, 54, 22, 62, 30,
          37, 5, 45, 13, 53, 21, 61, 29,
          36, 4, 44, 12, 52, 20, 60, 28,
          35, 3, 43, 11, 51, 19, 59, 27,
          34, 2, 42, 10, 50, 18, 58, 26]

# Expansion (for 32-bit -> 48-bit)
EP = [32, 1, 2, 3, 4, 5, 4, 5, 6, 7,
      8, 9, 8, 9, 10, 11, 12, 13, 12, 13,
      14, 15, 16, 17, 16, 17, 18, 19, 20, 21,
      20, 21, 22, 23, 24, 25, 24, 25, 26, 27,
      28, 29, 28, 29, 30, 31, 32, 1]

# Permutation P4 (used in S-box)
P4 = [2, 4, 3, 1]

# S-boxes
S0 = [[1, 0, 3, 2], [3, 2, 1, 0], [0, 2, 1, 3], [3, 1, 3, 2]]
S1 = [[0, 1, 2, 3], [2, 0, 1, 3], [3, 0, 1, 0], [2, 1, 0, 3]]

# Key schedule
P10 = [3, 5, 2, 7, 4, 10, 1, 9, 8, 6]
P8 = [6, 3, 7, 4, 8, 5, 10, 9]

# Helper Functions
def permute(bits, pattern):
    return [bits[i-1] for i in pattern]

def left_shift(bits, n):
    return bits[n:] + bits[:n]

def xor(bits1, bits2):
    return [b1 ^ b2 for b1, b2 in zip(bits1, bits2)]

def sbox_lookup(bits, sbox):
    row = (bits[0] << 1) | bits[3]
    col = (bits[1] << 1) | bits[2]
    val = sbox[row][col]
    return [val >> 1 & 1, val & 1]

def generate_keys(key):
    key = permute(key, P10)
    left, right = key[:5], key[5:]

    left = left_shift(left, 1)
    right = left_shift(right, 1)
    k1 = permute(left + right, P8)

    left = left_shift(left, 2)
    right = left_shift(right, 2)
    k2 = permute(left + right, P8)

    return k1, k2

def fk(bits, key):
    left, right = bits[:4], bits[4:]
    expanded = permute(right, EP)
    temp = xor(expanded, key)

    left_sbox = sbox_lookup(temp[:4], S0)
    right_sbox = sbox_lookup(temp[4:], S1)
    sbox_output = permute(left_sbox + right_sbox, P4)

    return xor(left, sbox_output) + right

def des_encrypt(plaintext, key):
    k1, k2 = generate_keys(key)
    bits = permute(plaintext, IP)
    bits = fk(bits, k1)
    bits = bits[4:] + bits[:4]
    bits = fk(bits, k2)
    return permute(bits, IP_INV)

def des_decrypt(ciphertext, key):
    k1, k2 = generate_keys(key)
    bits = permute(ciphertext, IP)
    bits = fk(bits, k2)
    bits = bits[4:] + bits[:4]
    bits = fk(bits, k1)
    return permute(bits, IP_INV)

def str_to_bits(s, size=8):
    return [int(b) for b in f"{s:0{size}b}"]

def bits_to_str(bits):
    return int("".join(map(str, bits)), 2)

def run_full_des_demo():
    print("\n=== Full DES (Data Encryption Standard) Demo ===")
    
    plaintext = str_to_bits(0b1010101010101010)
    key = str_to_bits(0b1010000010, size=10)

    print(f"Plaintext: {bits_to_str(plaintext):016b}")
    print(f"Key:       {bits_to_str(key):010b}")

    cipher = des_encrypt(plaintext, key)
    print(f"Ciphertext: {bits_to_str(cipher):016b}")

    decrypted = des_decrypt(cipher, key)
    print(f"Decrypted:  {bits_to_str(decrypted):016b}")

if __name__ == "__main__":
    run_full_des_demo()