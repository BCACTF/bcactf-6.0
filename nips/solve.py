#!/usr/bin/env python3
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
    flag = b"NIPS{S3lf_M0d1fy1ng_MIPS}"
    key_schedule = [0xDEADBEEF, 0xCAFEBABE, 0xFEEDFACE, 0xC0DEFEED]
    
    # Pad to 32 bytes
    null_byte = b'\x00'
    padded = flag + null_byte * (32 - len(flag))
    
    encrypted = bytearray()
    for i in range(0, len(padded), 8):
        block = padded[i:i+8]
        v = list(struct.unpack("<II", block))
        encrypted_v = tea_encrypt(v, key_schedule)
        encrypted.extend(struct.pack("<II", *encrypted_v))
    
    return encrypted[:24]  # Only first 24 bytes as expected

if __name__ == "__main__":
    result = solve()
    print(result.decode('latin-1', errors='ignore'))
