def generate_key(username1, username2):
    key = []
    length = max(len(username1), len(username2))

    # Step 1: XOR corresponding characters from both usernames
    for i in range(length):
        byte1 = ord(username1[i]) if i < len(username1) else 0
        byte2 = ord(username2[i]) if i < len(username2) else 0

        xor_result = byte1 ^ byte2
        key.append(xor_result)

    # Step 2: Perform bit shift (left rotate)
    for i in range(len(key)):
        key[i] = ((key[i] << (i % 8)) | (key[i] >> (8 - (i % 8)))) & 0xFF  # left rotate

    # Step 3: Reverse the order of the key
    key.reverse()

    return key


def decrypt_text(encrypted_text_hex, username1, username2):
    encrypted_data = bytes.fromhex(encrypted_text_hex)
    key = generate_key(username1, username2)

    decrypted_data = bytearray(len(encrypted_data))
    for i in range(len(encrypted_data)):
        decrypted_data[i] = encrypted_data[i] ^ key[i % len(key)]

    return decrypted_data.decode("utf-8")


# Sample input
username1 = "hun73r12"
username2 = "__purten75"
encrypted_text_hex = "08544f76b472694f3c03045c1b4aa6246027635f59684626f1644d016442355a5b20f74b2a4b0b5a13684026b74b2a4b610035515c24f37a7605"  # This will be the encrypted hex string from the C++ program

# Decrypt the text
decrypted_text = decrypt_text(encrypted_text_hex, username1, username2)
print(f"Decrypted Text: {decrypted_text}")
