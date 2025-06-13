def solve_flag():
    # Constants from the contract
    K1 = bytes.fromhex("c5d71484f8cf9bf4b76f47904730804b")
    OB1 = bytes.fromhex("a8b576e88daae1c2885f77f57702fa15")
    
    K2 = bytes.fromhex("9e3225a9f133b5dea168f4e2851f072f")
    OB2 = bytes.fromhex("10659bdc6368e83dd4d62a13f3523aa1")
    
    K3 = bytes.fromhex("cc00fcaa7ca62061717a48e5")
    OB3 = bytes.fromhex("ff64a39c4c96443e1b4a7098")
    
    SUM_CHECK = 260
    
    flag = bytearray(44)
    
    # Reverse Group 1: Subtract 1 from OB1 and XOR with K1
    for i in range(16):
        flag[i] = ((OB1[i] - 1) & 0xFF) ^ K1[i]
    
    # Reverse Group 2: Subtract K2 from OB2 with modular arithmetic
    for i in range(16):
        flag[i + 16] = (OB2[i] - K2[i]) & 0xFF
    
    # Reverse Group 3: XOR OB3 with K3 (XOR is its own inverse)
    for i in range(12):
        flag[i + 32] = OB3[i] ^ K3[i]
    
    # Verify the sum constraint
    sum3 = flag[4] + flag[10] + flag[15]
    print(f"Sum of bytes at indices 4, 10, 15: {sum3}, Required: {SUM_CHECK}")
    
    try:
        result = bytes(flag).decode('ascii')
        print(f"Found flag: {result}")
        return result
    except UnicodeDecodeError:
        print("Warning: Result contains non-ASCII characters")
        return bytes(flag).hex()

# Run the solver
flag = solve_flag()
