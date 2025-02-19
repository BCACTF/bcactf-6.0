def unscramble_flag(scrambled):
    # Reverse the steps of the scramble_flag function
    reversed_scrambled = scrambled.replace(' ', '_')  # Replace spaces with underscores
    original = ''.join([char.swapcase() for char in reversed_scrambled[::-1]])  # Reverse and swap case
    return original

# Read the scrambled flag from flag.txt
with open("flag.txt", "r") as f:
    scrambled_flag = f.read().strip()

# Unscramble the flag
unscrambled_flag = unscramble_flag(scrambled_flag)

print(f"Scrambled flag: {scrambled_flag}")
print(f"Unscrambled flag: {unscrambled_flag}")
