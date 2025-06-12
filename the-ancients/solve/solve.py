def recover_flag(output_string):
    # Constants from the JavaScript
    key1 = 7
    key2 = 13
    
    # Step 1: Parse the output string into numbers
    reversed_values = []
    i = 0
    while i < len(output_string):
        num = int(output_string[i:i+2])
        reversed_values.append(num)
        i += 2
    
    print(f"Parsed values: {reversed_values}")
    
    # Step 2: Reverse the reversal (undo Step 3 from the encoder)
    transformed = reversed_values[::-1]
    print(f"After undoing reversal: {transformed}")
    
    # Step 3: Unswap the pairs (undo Step 2 from the encoder)
    i = 0
    while i < len(transformed) - 1:
        temp = transformed[i]
        transformed[i] = transformed[i + 1]
        transformed[i + 1] = temp
        i += 2
    
    print(f"After unswapping pairs: {transformed}")
    
    # Step 4: Reverse the character transformation (undo Step 1)
    original_chars = []
    for i in range(len(transformed)):
        val = transformed[i]
        # Undo: ((code ^ i) + key1) ^ key2
        # First undo XOR with key2
        val = val ^ key2
        # Then subtract key1
        val = val - key1
        # Finally undo XOR with position
        val = val ^ i
        original_chars.append(val)
    
    print(f"Recovered character codes: {original_chars}")
    
    # Convert to characters
    flag = ''.join(chr(c) for c in original_chars)
    print(f"Recovered flag: {flag}")
    
    return flag

# Test the recovery with the given output
output = "4580468869842695137918720122621186265114611409710211437891229133757610084119757999137122122103103106100100"
recovered_flag = recover_flag(output)

# Verify the recovery by re-encoding
def verify_encoding(flag):
    key1 = 7
    key2 = 13
    transformed = []
    
    # Step 1: Transform characters
    for i in range(len(flag)):
        code = ord(flag[i])
        transformed_val = ((code ^ i) + key1) ^ key2
        transformed.append(transformed_val)
    
    # Step 2: Swap pairs
    i = 0
    while i < len(transformed) - 1:
        transformed[i], transformed[i + 1] = transformed[i + 1], transformed[i]
        i += 2
    
    # Step 3: Reverse array
    transformed = transformed[::-1]
    
    # Step 4: Create output string
    result = ''
    for num in transformed:
        result += f"{num:02d}"
    
    return result

# Verify our solution
encoded = verify_encoding(recovered_flag)
print(f"Original output: {output}")
print(f"Re-encoded output: {encoded}")
print(f"Match: {encoded == output}")
