#!/usr/bin/env python3
import sys

def generate_constants(flag):
    """Generate encrypted constants for the Go binary"""
    
    # Stage 1: Simple XOR with rotating key
    stage1_key = [0x42, 0x13, 0x37, 0x89, 0xAB, 0xCD, 0xEF, 0x21]
    stage1_encrypted = []
    for i, byte in enumerate(flag.encode()):
        stage1_encrypted.append(byte ^ stage1_key[i % len(stage1_key)])
    
    # Stage 2: Add/subtract with alternating pattern
    stage2_encrypted = []
    for i, byte in enumerate(stage1_encrypted):
        if i % 2 == 0:
            stage2_encrypted.append((byte + 0x17) & 0xFF)
        else:
            stage2_encrypted.append((byte - 0x23) & 0xFF)
    
    # Stage 3: Bit rotation
    final_encrypted = []
    for i, byte in enumerate(stage2_encrypted):
        # Rotate left by (i % 8) positions
        rot = i % 8
        if rot == 0:
            rotated = byte
        else:
            rotated = ((byte << rot) | (byte >> (8 - rot))) & 0xFF
        final_encrypted.append(rotated)
    
    # Generate Go constants
    print("// Generated constants - paste into main.go")
    print("var encryptedFlag = []byte{", end="")
    for i, byte in enumerate(final_encrypted):
        if i % 8 == 0:
            print("\n\t", end="")
        print(f"0x{byte:02x}, ", end="")
    print("\n}")
    
    print(f"\nvar flagLength = {len(flag)}")
    
    # Verification - decrypt to make sure it works
    print("\n// Verification:")
    decrypted = decrypt_flag(final_encrypted)
    print(f"// Original: {flag}")
    print(f"// Decrypted: {decrypted}")
    print(f"// Match: {flag == decrypted}")

def decrypt_flag(encrypted):
    """Verify decryption works correctly"""
    
    # Stage 1: Reverse bit rotation
    stage1 = []
    for i, byte in enumerate(encrypted):
        rot = i % 8
        if rot == 0:
            rotated = byte
        else:
            rotated = ((byte >> rot) | (byte << (8 - rot))) & 0xFF
        stage1.append(rotated)
    
    # Stage 2: Reverse add/subtract operations
    stage2 = []
    for i, byte in enumerate(stage1):
        if i % 2 == 0:
            stage2.append((byte - 0x17) & 0xFF)
        else:
            stage2.append((byte + 0x23) & 0xFF)
    
    # Stage 3: Reverse XOR with rotating key
    xor_key = [0x42, 0x13, 0x37, 0x89, 0xAB, 0xCD, 0xEF, 0x21]
    final = []
    for i, byte in enumerate(stage2):
        final.append(byte ^ xor_key[i % len(xor_key)])
    
    return bytes(final).decode()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 genconst.py <flag>")
        sys.exit(1)
    
    flag = sys.argv[1]
    generate_constants(flag)
