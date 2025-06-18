import os
import sys
import random
import string

def corrupt_word(word, bit):
    """
    Corrupt a word by modifying one letter based on the bit value.
    If bit is 1, shift a random letter forward in the alphabet.
    If bit is 0, shift a random letter backward in the alphabet.
    """
    if len(word) <= 2:  # Skip words that are too short to corrupt
        return None  # Indicate that this word cannot be corrupted

    # Find a random index to corrupt (not the first or last character)
    valid_indices = [i for i in range(1, len(word) - 1) if word[i].isalpha()]
    if not valid_indices:
        return None  # Indicate that this word cannot be corrupted

    index = random.choice(valid_indices)
    char = word[index]

    if char.isalpha():
        if bit == '1':
            # Shift forward in the alphabet
            new_char = chr((ord(char.lower()) - ord('a') + 1) % 26 + ord('a'))
        else:
            # Shift backward in the alphabet
            new_char = chr((ord(char.lower()) - ord('a') - 1) % 26 + ord('a'))

        # Preserve case
        new_char = new_char.upper() if char.isupper() else new_char
        word = word[:index] + new_char + word[index + 1:]

    return word

def corrupt_text(input_text, binary_string):
    """
    Corrupt the input text based on the binary string.
    Ensures every binary bit is used in order and corruption is dispersed.
    """
    words = input_text.split()
    corrupted_words = []
    binary_index = 0

    for word in words:
        # If the binary string has been fully used, wrap around
        bit = binary_string[binary_index % len(binary_string)]

        # Attempt to corrupt the word
        corrupted_word = corrupt_word(word, bit)
        if corrupted_word is not None:
            corrupted_words.append(corrupted_word)
            binary_index += 1  # Move to the next binary bit
        else:
            # If the word couldn't be corrupted, add it as is
            corrupted_words.append(word)

        # If all binary bits are used, continue processing the rest of the words
        if binary_index >= len(binary_string):
            corrupted_words.extend(words[len(corrupted_words):])
            break

    return ' '.join(corrupted_words)

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <input_file> <binary_string>")
        sys.exit(1)

    input_file = sys.argv[1]
    binary_string = sys.argv[2]

    # Validate binary string
    if not all(bit in '01' for bit in binary_string):
        print("Error: Binary string must contain only 0s and 1s.")
        sys.exit(1)

    # Read the input file
    if not os.path.exists(input_file):
        print(f"Error: File '{input_file}' does not exist.")
        sys.exit(1)

    with open(input_file, 'r') as file:
        input_text = file.read().strip()

    # Corrupt the text
    corrupted_text = corrupt_text(input_text, binary_string)

    # Output the corrupted text
    output_file = f"corrupted_{os.path.basename(input_file)}"
    with open(output_file, 'w') as file:
        file.write(corrupted_text)

    print(f"Corrupted text written to '{output_file}'.")

if __name__ == "__main__":
    main()
