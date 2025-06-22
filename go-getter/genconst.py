#!/usr/bin/env python3
import sys

def encrypt_flag(flag):
    """Encrypt flag with a simple but effective multi-stage process"""
    data = flag.encode()
    
    # Stage 1: XOR with key
    key1 = [0x13, 0x37, 0x42, 0x69, 0x88, 0xAA, 0xBB, 0xCC]
    stage1 = []
    for i, b in enumerate(data):
        stage1.append(b ^ key1[i % len(key1)])
    
    # Stage 2: Add with rotating offset
    stage2 = []
    for i, b in enumerate(stage1):
        offset = (i * 7 + 23) & 0xFF
        stage2.append((b + offset) & 0xFF)
    
    # Stage 3: Swap nibbles and XOR with position
    final = []
    for i, b in enumerate(stage2):
        # Swap high and low nibbles
        swapped = ((b & 0x0F) << 4) | ((b & 0xF0) >> 4)
        # XOR with position-based value
        pos_xor = (i * 3 + 0x55) & 0xFF
        final.append(swapped ^ pos_xor)
    
    return final

def decrypt_flag(encrypted):
    """Decrypt flag - reverse of encrypt_flag"""
    # Stage 1: Reverse nibble swap and position XOR
    stage1 = []
    for i, b in enumerate(encrypted):
        # Reverse position XOR
        pos_xor = (i * 3 + 0x55) & 0xFF
        unxored = b ^ pos_xor
        # Reverse nibble swap
        original = ((unxored & 0x0F) << 4) | ((unxored & 0xF0) >> 4)
        stage1.append(original)
    
    # Stage 2: Subtract rotating offset
    stage2 = []
    for i, b in enumerate(stage1):
        offset = (i * 7 + 23) & 0xFF
        stage2.append((b - offset) & 0xFF)
    
    # Stage 3: Reverse XOR with key
    key1 = [0x13, 0x37, 0x42, 0x69, 0x88, 0xAA, 0xBB, 0xCC]
    final = []
    for i, b in enumerate(stage2):
        final.append(b ^ key1[i % len(key1)])
    
    return bytes(final).decode()

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 genconst.py <flag>")
        sys.exit(1)
    
    flag = sys.argv[1]
    encrypted = encrypt_flag(flag)
    
    print("// Generated constants for main.go")
    print("var encryptedFlag = []byte{")
    for i in range(0, len(encrypted), 8):
        chunk = encrypted[i:i+8]
        line = "\t" + ", ".join(f"0x{b:02x}" for b in chunk) + ","
        print(line)
    print("}")
    print(f"var flagLength = {len(flag)}")
    
    # Verify
    decrypted = decrypt_flag(encrypted)
    print(f"\n// Verification:")
    print(f"// Original:  {flag}")
    print(f"// Decrypted: {decrypted}")
    print(f"// Match: {flag == decrypted}")

if __name__ == "__main__":
    main()
