import struct
from typing import List

# TEA constants
TEA_DELTA = 0x9E3779B9
TEA_ROUNDS = 32

# Cipher data and key
CIPHER_HEX = (
    "45A8D67F79B2E728E8C51B244FC5D7F7"
    "549BA908909F81EC0F841FC39715F955"
)

KEY = [0xDEADBEEF, 0xCAFEBABE, 0xFEEDFACE, 0xC0DEFEED]


def tea_decrypt_block(encrypted_block: bytes, key: List[int]) -> bytes:
    """
    Decrypt a single 8-byte block using the TEA algorithm.
    
    Args:
        encrypted_block: 8-byte block to decrypt
        key: List of 4 32-bit integers used as the decryption key
    
    Returns:
        Decrypted 8-byte block
    """
    # Unpack the block into two 32-bit unsigned integers (little-endian)
    v0, v1 = struct.unpack('<II', encrypted_block)
    
    # Initialize sum for decryption (sum after all encryption rounds)
    sum_value = (TEA_DELTA * TEA_ROUNDS) & 0xFFFFFFFF
    
    # Perform 32 decryption rounds
    for _ in range(TEA_ROUNDS):
        v1 = (v1 - (((v0 << 4) + key[2]) ^ (v0 + sum_value) ^ ((v0 >> 5) + key[3]))) & 0xFFFFFFFF
        v0 = (v0 - (((v1 << 4) + key[0]) ^ (v1 + sum_value) ^ ((v1 >> 5) + key[1]))) & 0xFFFFFFFF
        sum_value = (sum_value - TEA_DELTA) & 0xFFFFFFFF
    
    # Pack the decrypted values back into bytes
    return struct.pack('<II', v0, v1)


def tea_decrypt(ciphertext: bytes, key: List[int]) -> bytes:
    """
    Decrypt data using TEA algorithm.
    
    Args:
        ciphertext: Encrypted data (must be multiple of 8 bytes)
        key: List of 4 32-bit integers used as the decryption key
    
    Returns:
        Decrypted plaintext
    """
    if len(ciphertext) % 8 != 0:
        raise ValueError("Ciphertext length must be a multiple of 8 bytes")
    
    # Decrypt each 8-byte block
    decrypted_blocks = []
    for i in range(0, len(ciphertext), 8):
        block = ciphertext[i:i+8]
        decrypted_blocks.append(tea_decrypt_block(block, key))
    
    return b''.join(decrypted_blocks)


def main():
    """Main execution function."""
    # Convert hex string to bytes
    cipher_bytes = bytes.fromhex(CIPHER_HEX)
    
    # Decrypt the data
    plaintext = tea_decrypt(cipher_bytes, KEY)
    
    # Remove null padding and decode to string
    result = plaintext.rstrip(b'\0').decode('utf-8')
    print(result)


if __name__ == "__main__":
    main()
