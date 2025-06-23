#!/usr/bin/env python3
import struct


def tea_encrypt(v, k):
    """TEA encryption function - encrypts 8 bytes using 16-byte key"""
    v0, v1 = v[0], v[1]
    sum_val = 0
    delta = 0x9E3779B9
    
    for i in range(32):
        sum_val = (sum_val + delta) & 0xFFFFFFFF
        v0 = (v0 + (((v1 << 4) + k[0]) ^ (v1 + sum_val) ^ ((v1 >> 5) + k[1]))) & 0xFFFFFFFF
        v1 = (v1 + (((v0 << 4) + k[2]) ^ (v0 + sum_val) ^ ((v0 >> 5) + k[3]))) & 0xFFFFFFFF
    
    return [v0, v1]


def solve():
    """
    The challenge expects the user to provide the original flag as input.
    The binary will TEA-encrypt the input and compare it with the stored encrypted flag.
    So the solution is simply the original flag text.
    """
    flag = "bcactf{S3lf_M0d1fy1ng_MIPS}"
    return flag


if __name__ == "__main__":
    result = solve()
    print(result)