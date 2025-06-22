from itertools import product
from morse_encodings import MORSE_CODE

# Fractionated Morse Cipher implementation in Python
# 26 lowercase + 26 uppercase + 10 numbers + "_' + "Þ" = 64 characters

keys = list(MORSE_CODE.keys())

# for i in range(0, len(MORSE_CODE) - 1): # Adds lowercase letters
#     MORSE_CODE[keys[i].lower()] = ';' + MORSE_CODE[keys[i]]

print(MORSE_CODE)

# All possible quadgraphs of '.', '-', 'x', ';'

QUADGRPAHS = [''.join(p) for p in product('.-x;', repeat=3)]
print(len(QUADGRPAHS))
# Default key (can be changed)
KEY = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_Þ"

def unwrap_flag(flag):
    return flag[7:-1]

def gen_fmc_table(key=KEY):
    # Remove duplicates, keep order
    seen = set()
    key = ''.join([c for c in key if not (c in seen or seen.add(c))])
    # Fill with rest of alphabet/numbers
    rest = ''.join([c for c in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789_Þ" if c not in key])
    table = key + rest
    return dict(zip(QUADGRPAHS, table[:len(QUADGRPAHS)])), dict(zip(table[:len(QUADGRPAHS)], QUADGRPAHS))

def text_to_morse(text):
    return ''.join(MORSE_CODE.get(c, '') for c in text)

def pad_morse(morse):
    # Pad with 'x' to make length a multiple of 3
    return morse + 'x' * (3 - (len(morse) % 3))

def fractionate(morse):
    return [morse[i:i+3] for i in range(0, len(morse), 3)]

def encrypt(plaintext, key=KEY):
    enc_table, _ = gen_fmc_table(key)
    print(enc_table)
    morse = text_to_morse(plaintext)
    morse = pad_morse(morse)
    quadgraphs = fractionate(morse)
    print(''.join(quadgraphs))
    return ''.join(enc_table.get(tri, '?') for tri in quadgraphs)

def decrypt(ciphertext, key=KEY):
    _, dec_table = gen_fmc_table(key)
    morse = ''.join(dec_table.get(c, '') for c in ciphertext)
    # Split morse by 'x' (space)
    words = morse.split('x')
    # Reverse MORSE_CODE
    rev_morse = {v: k for k, v in MORSE_CODE.items()}
    result = []
    for word in words:
        i = 0
        decoded = ''
        while i < len(word):
            for l in range(5, 0, -1):  # Morse code max length is 5
                if word[i:i+l] in rev_morse:
                    decoded += rev_morse[word[i:i+l]]
                    i += l
                    break
            else:
                i += 1  # skip unknown
        result.append(decoded)
    return '_'.join(result)

# Example usage:
if __name__ == "__main__":
    # msg = "HELLO"
    # key = "SECRETKEY"
    # enc = encrypt(msg, key)
    # print("Encrypted:", enc)
    # dec = decrypt(enc, key)
    # print("Decrypted:", dec)
    with open('flag.txt', encoding='utf-8') as f:
        unwrapped_flag = unwrap_flag(f.read())
        print(unwrapped_flag)
        provided_key = "SwampMarshBogFen"
        enc_res = encrypt(unwrapped_flag, provided_key)
        dec_res = decrypt(enc_res, provided_key)
        print(enc_res + "\n" + dec_res)
