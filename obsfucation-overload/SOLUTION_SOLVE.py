# Function to reverse the simple encryption
def simple_decrypt(encrypted_data, key):
    decrypted_data = []
    for i in range(len(encrypted_data)):
        # Reverse the +0x10 operation
        b = (encrypted_data[i] - 0x10) & 0xFF
        # Reverse XOR with the key
        b ^= key[i % len(key)]
        decrypted_data.append(b)
    return decrypted_data

# Reverse the 0x2A XOR encoding of the flag
def decode_flag(encrypted_data, key):
    decrypted_data = simple_decrypt(encrypted_data, key)

    # Reverse XOR with 0x2A
    flag = ''.join([chr(b ^ 0x2A) for b in decrypted_data])
    return flag

# The identifier used to generate the key
identifier = "test"  # Replace with the actual identifier used in the challenge
seed = identifier + "_bcactf2025"
seed = seed[::-1]  # Reverse the seed string

# Apply bitwise NOT and convert to a key
seed = ''.join([chr((~ord(c)) & 0xFF) for c in seed])  # Apply bitwise NOT

key = [ord(c) for c in seed[:8]]

# Read the encrypted payload from the 'payload.dat' file
with open("payload.dat", "rb") as f:
    encrypted_data = list(f.read())

# Decode the flag using the decryption function
decoded_flag = decode_flag(encrypted_data, key)

# Output the flag
print(f"Decoded Flag: {decoded_flag}")