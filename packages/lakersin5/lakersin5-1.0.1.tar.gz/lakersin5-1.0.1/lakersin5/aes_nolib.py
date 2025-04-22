# lakersin5/aes_without_lib.py

# Predefined S-box for SubBytes step
S_BOX = [
    [0x63, 0x7c, 0x77, 0x7b, 0xf0, 0x6b, 0x6f, 0xc5],
    [0x30, 0x01, 0x67, 0x2b, 0xfe, 0xd7, 0xab, 0x76],
    [0xca, 0x82, 0xc9, 0x7d, 0xFA, 0x59, 0x47, 0xf0],
    [0x33, 0x88, 0x43, 0x20, 0x5f, 0x75, 0x4b, 0x9a]
]

# The AES Round Constant (used in the key expansion process)
RCON = [0x01, 0x02, 0x04, 0x08, 0x10, 0x20, 0x40, 0x80, 0x1b, 0x36]

# Helper Functions
def sub_bytes(state):
    """Substitute bytes in state using S-box."""
    return [[S_BOX[i][j] for j in range(4)] for i in range(4)]

def shift_rows(state):
    """Shift rows of the state matrix."""
    return [
        state[0],
        state[1][1:] + state[1][:1],
        state[2][2:] + state[2][:2],
        state[3][3:] + state[3][:3],
    ]

def mix_columns(state):
    """Mix the columns of the state matrix."""
    # Using a simplified mix matrix for educational purposes
    mix = [
        [0x02, 0x03, 0x01, 0x01],
        [0x01, 0x02, 0x03, 0x01],
        [0x01, 0x01, 0x02, 0x03],
        [0x03, 0x01, 0x01, 0x02]
    ]
    result = [[0]*4 for _ in range(4)]
    for i in range(4):
        for j in range(4):
            result[i][j] = sum(mix[i][k] * state[k][j] for k in range(4)) % 0x100
    return result

def add_round_key(state, key_schedule, round_num):
    """Add round key by XORing the state with the round key."""
    key = key_schedule[round_num]
    for i in range(4):
        for j in range(4):
            state[i][j] ^= key[i][j]
    return state

def key_expansion(key):
    """Expand the key into 44 words for AES-128 (11 rounds)."""
    key_schedule = [key[i:i + 4] for i in range(0, 16, 4)]
    for round_num in range(4, 44):
        temp = key_schedule[round_num - 1]
        if round_num % 4 == 0:
            # RotWord
            temp = temp[1:] + temp[:1]
            # SubWord (apply S-box)
            temp = [S_BOX[b // 16][b % 16] for b in temp]
            # XOR with round constant
            temp[0] ^= RCON[round_num // 4 - 1]
        key_schedule.append([key_schedule[round_num - 4][i] ^ temp[i] for i in range(4)])
    return key_schedule

def aes_encrypt(plaintext, key):
    """Encrypt 16-byte plaintext using AES-128."""
    # Convert key and plaintext into state matrices (4x4)
    state = [list(plaintext[i:i + 4]) for i in range(0, 16, 4)]
    
    # Key expansion
    key_schedule = key_expansion(key)
    
    # Initial round key addition
    state = add_round_key(state, key_schedule, 0)
    
    # Main rounds
    for round_num in range(1, 10):
        state = sub_bytes(state)
        state = shift_rows(state)
        state = mix_columns(state)
        state = add_round_key(state, key_schedule, round_num)
    
    # Final round (without MixColumns)
    state = sub_bytes(state)
    state = shift_rows(state)
    state = add_round_key(state, key_schedule, 10)
    
    # Convert state back to bytes
    return bytes([state[i][j] for i in range(4) for j in range(4)])

def aes_decrypt(ciphertext, key):
    """Decrypt AES-128 ciphertext."""
    # Same procedure but reversing the operations
    # This would require inverse of SubBytes, ShiftRows, MixColumns, and key expansion
    
    # For simplicity, decryption isn't shown here, but it follows a similar pattern as encryption
    pass

def run_aes_demo():
    print("\n=== AES-128 Encryption/Decryption Demo (without libraries) ===")

    # Example key (16 bytes for AES-128)
    key = [0x2b, 0x7e, 0x15, 0x16, 0x28, 0xae, 0xd2, 0xa6, 0xab, 0xf7, 0x97, 0x75, 0x46, 0x34, 0x49, 0x43]

    # Example plaintext (16 bytes)
    plaintext = [0x32, 0x88, 0x31, 0xe0, 0x43, 0x5a, 0x31, 0x37, 0xf6, 0x30, 0x98, 0x07, 0xa8, 0x8d, 0xa2, 0x34]

    print(f"Key:       {''.join(format(x, '02x') for x in key)}")
    print(f"Plaintext: {''.join(format(x, '02x') for x in plaintext)}")

    # Encrypt the plaintext
    ciphertext = aes_encrypt(plaintext, key)
    print(f"Ciphertext: {''.join(format(x, '02x') for x in ciphertext)}")

if __name__ == "__main__":
    run_aes_demo()