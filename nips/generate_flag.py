#!/usr/bin/env python3
import struct
import sys


def encrypt_flag(flag, key_schedule):
    # Ensure the flag is a multiple of 8 bytes
    if len(flag) % 8 != 0:
        flag += b"\x00" * (8 - (len(flag) % 8))

    encrypted = bytearray()

    # Process the flag in 8-byte blocks
    for i in range(0, len(flag), 8):
        block = flag[i : i + 8]
        v = list(struct.unpack("<II", block))  # Convert to two 32-bit integers

        # Apply the TEA cipher (32 rounds for security)
        sum = 0
        delta = 0x9E3779B9
        for j in range(32):
            sum = (sum + delta) & 0xFFFFFFFF
            v[0] = (
                v[0]
                + (
                    ((v[1] << 4) + key_schedule[0])
                    ^ (v[1] + sum)
                    ^ ((v[1] >> 5) + key_schedule[1])
                )
            ) & 0xFFFFFFFF
            v[1] = (
                v[1]
                + (
                    ((v[0] << 4) + key_schedule[2])
                    ^ (v[0] + sum)
                    ^ ((v[0] >> 5) + key_schedule[3])
                )
            ) & 0xFFFFFFFF

        # Convert back to bytes and add to result
        encrypted.extend(struct.pack("<II", v[0], v[1]))

    return encrypted


def decrypt_flag(encrypted, key_schedule):
    # Decrypt to verify our implementation
    decrypted = bytearray()

    # Process in 8-byte blocks
    for i in range(0, len(encrypted), 8):
        block = encrypted[i : i + 8]
        v = list(struct.unpack("<II", block))

        # Apply TEA decryption (32 rounds)
        sum = 0xC6EF3720  # delta * 32
        delta = 0x9E3779B9
        for j in range(32):
            v[1] = (
                v[1]
                - (
                    ((v[0] << 4) + key_schedule[2])
                    ^ (v[0] + sum)
                    ^ ((v[0] >> 5) + key_schedule[3])
                )
            ) & 0xFFFFFFFF
            v[0] = (
                v[0]
                - (
                    ((v[1] << 4) + key_schedule[0])
                    ^ (v[1] + sum)
                    ^ ((v[1] >> 5) + key_schedule[1])
                )
            ) & 0xFFFFFFFF
            sum = (sum - delta) & 0xFFFFFFFF

        decrypted.extend(struct.pack("<II", v[0], v[1]))

    return decrypted


def main():
    # The actual flag
    flag = b"bcactf{S3lf_M0d1fy1ng_MIPS}"

    # Key schedule
    key_schedule = [0xDEADBEEF, 0xCAFEBABE, 0xFEEDFACE, 0xC0DEFEED]

    # Encrypt the flag
    encrypted_flag = encrypt_flag(flag, key_schedule)

    # Verify by decrypting
    decrypted = decrypt_flag(encrypted_flag, key_schedule)
    null_byte = b"\x00"
    decrypted_clean = decrypted.rstrip(null_byte)
    print(f"Original: {flag}")
    print(f"Decrypted: {decrypted_clean}")
    print(f"Match: {flag == decrypted_clean}")
    print()

    # Print the encrypted flag as a C array
    print("unsigned char encrypted_flag[] = {")
    for i in range(0, len(encrypted_flag), 8):
        line = ", ".join(f"0x{b:02X}" for b in encrypted_flag[i : i + 8])
        if i + 8 < len(encrypted_flag):
            print(f"    {line},")
        else:
            print(f"    {line}")
    print("};")

    # Also generate the correct input that should be provided to the challenge
    print(f"\nCorrect input (encrypted flag): {encrypted_flag.hex()}")

    # Generate a solver script
    with open("solve.py", "w") as f:
        f.write(
            """#!/usr/bin/env python3
import struct

def tea_encrypt(v, k):
    v0, v1 = v[0], v[1]
    sum_val = 0
    delta = 0x9E3779B9
    
    for i in range(32):
        sum_val = (sum_val + delta) & 0xFFFFFFFF
        v0 = (v0 + (((v1 << 4) + k[0]) ^ (v1 + sum_val) ^ ((v1 >> 5) + k[1]))) & 0xFFFFFFFF
        v1 = (v1 + (((v0 << 4) + k[2]) ^ (v0 + sum_val) ^ ((v0 >> 5) + k[3]))) & 0xFFFFFFFF
    
    return [v0, v1]

def solve():
    flag = b"bcactf{S3lf_M0d1fy1ng_MIPS}"
    key_schedule = [0xDEADBEEF, 0xCAFEBABE, 0xFEEDFACE, 0xC0DEFEED]
    
    # Pad to 32 bytes
    null_byte = b'\\x00'
    padded = flag + null_byte * (32 - len(flag))
    
    encrypted = bytearray()
    for i in range(0, len(padded), 8):
        block = padded[i:i+8]
        v = list(struct.unpack("<II", block))
        encrypted_v = tea_encrypt(v, key_schedule)
        encrypted.extend(struct.pack("<II", *encrypted_v))
    
    return encrypted[:26]  # Only first 26 bytes as expected

if __name__ == "__main__":
    result = solve()
    print(result.decode('latin-1', errors='ignore'))
"""
        )


if __name__ == "__main__":
    main()
