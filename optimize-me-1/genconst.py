#!/usr/bin/env python3
import hashlib

def generate_flag_constants():
    flag = "bcactf{0pt1m1z4t10n_m4st3r_2025}"
    
    # Convert flag to bytes and create encrypted constants
    flag_bytes = flag.encode('utf-8')
    constants = []
    keys = []
    
    print("// Generated encrypted flag constants")
    print("const unsigned char encrypted_flag[] = {", end="")
    
    for i, byte in enumerate(flag_bytes):
        # Simple XOR encryption with position-based key
        key = (i * 37 + 42) % 256
        encrypted = byte ^ key
        constants.append(encrypted)
        keys.append(key)
        
        if i > 0:
            print(",", end="")
        print(f" 0x{encrypted:02x}", end="")
    
    print(" };")
    print(f"const int flag_length = {len(flag_bytes)};")
    
    # Generate key derivation constants
    print("\n// Key derivation constants")
    print("const int key_multiplier = 37;")
    print("const int key_offset = 42;")
    
    # Verification
    print(f"\n// Original flag: {flag}")
    print("// Decryption verification:")
    decrypted = ""
    for i, enc in enumerate(constants):
        key = (i * 37 + 42) % 256
        dec = enc ^ key
        decrypted += chr(dec)
    print(f"// Decrypted: {decrypted}")

if __name__ == "__main__":
    generate_flag_constants()
