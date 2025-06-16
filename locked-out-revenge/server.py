#!/usr/bin/env python3

allowed = set("abcde") # GRR only 5 chars now
allowed_nonalpha_FULL = list( "\"'()=+:;. 1234567890")
allowed_nonalpha = allowed_nonalpha_FULL[:5] # GRR u only get 5 of these too

code = input(">>> ")

broke_the_rules = False
for c in code:
    if c.lower() not in allowed and c not in allowed_nonalpha:
        print(f"Character {c} not allowed!")
        broke_the_rules = True
        break
    allowed = set(chr((ord(a) - ord('a') + 1) % 26 + ord('a')) for a in allowed)
    allowed_nonalpha = [allowed_nonalpha_FULL[idx] for idx in [(idx + 1) % len(allowed_nonalpha_FULL) for idx in [allowed_nonalpha_FULL.index(char) for char in allowed_nonalpha]]] # holy list comprehension

if not broke_the_rules:
    exec(code)
