def scramble_flag(flag):
    # Reverse the string, swap case, and replace underscores with spaces
    scrambled = ''.join([char.swapcase() for char in flag[::-1]])
    return scrambled.replace('_', ' ')  # Replace only underscores with spaces

# Your flag (the answer to the challenge)
flag = "BCACTF{r3v3Rs3_ThIs_To_wIn}"

# Scramble the flag
scrambled_flag = scramble_flag(flag)

# Save the scrambled flag
with open("flag.txt", "w") as f:
    f.write(scrambled_flag)

print("Scrambled flag created! Check flag.txt for the scrambled string.")
