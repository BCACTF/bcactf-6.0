import os
import sys


INPUT_TXT = input("give the filename of the unedited, correctly spelled, txt file: ").strip()
with open(INPUT_TXT, 'r') as file:
    INPUT_TEXT = file.read().strip()

INPUT_WORDS = INPUT_TEXT.replace("\n", " ").replace("  ", " ").split()
print(len(INPUT_WORDS))
print(INPUT_WORDS)
