#!/usr/bin/env python3
import struct
import sys

def encrypt_flag(flag, key_schedule):
    # Ensure the flag is a multiple of 8 bytes
    if len(flag) % 8 != 0:
        flag += b'\x00' * (8 - (len(flag) % 8))
    
    encrypted = bytearray()
    
    # Process the flag in 8-byte blocks
    for i in range(0, len(flag), 8):
        block = flag[i:i+8]
        v = list(struct.unpack("<II", block))  # Convert to two 32-bit integers
        
        # Apply the TEA-like cipher
        sum = 0
        delta = 0x9E3779B9
        for j in range(16):
            sum = (sum + delta) & 0xFFFFFFFF
            v[0] = (v[0] + (((v[1] << 4) + key_schedule[0]) ^ (v[1] + sum) ^ 
                   ((v[1] >> 5) + key_schedule[1]))) & 0xFFFFFFFF
            v[1] = (v[1] + (((v[0] << 4) + key_schedule[2]) ^ (v[0] + sum) ^ 
                   ((v[0] >> 5) + key_schedule[3]))) & 0xFFFFFFFF
        
        # Convert back to bytes and add to result
        encrypted.extend(struct.pack("<II", v[0], v[1]))
    
    return encrypted

def main():
    # The actual flag
    flag = b"NIPS{S3lf_M0d1fy1ng_MIPS}"
    
    # Key schedule
    key_schedule = [0xDEADBEEF, 0xCAFEBABE, 0xFEEDFACE, 0xC0DEFEED]
    
    # Encrypt the flag
    encrypted_flag = encrypt_flag(flag, key_schedule)
    
    # Print the encrypted flag as a C array
    print("unsigned char encrypted_flag[] = {")
    for i in range(0, len(encrypted_flag), 8):
        line = ", ".join(f"0x{b:02X}" for b in encrypted_flag[i:i+8])
        if i + 8 < len(encrypted_flag):
            print(f"    {line},")
        else:
            print(f"    {line}")
    print("};")

if __name__ == "__main__":
    main()
