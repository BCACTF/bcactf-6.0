import sys
import json
import random
import time

TIME_LIMIT = 10  # 10 seconds to solve em all!


def key_s2tring_random(xeno):
    spl = lambda word: [char for char in word]
    if xeno:
        A = spl("ABCDEFGHIJKLMNÑOPQRSTUVWXYZ")
    else:
        A = spl("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    while not test1(A):
        random.shuffle(A)
    return "".join(A)


def test1(l):
    for i in range(26):
        if ord(l[i]) - 65 == i:
            return False
    return True


def getRandWord(minlen, maxlen):
    with open("words.txt", "r") as f:
        for _ in range(random.randint(0, 9000)):
            f.readline()
        r = ""
        while len(r) < minlen or len(r) > maxlen:
            r = f.readline().strip()
    return r


def genQuotes(n):
    l = open("quotes.txt", "r", encoding="utf-8").read().split("\n")
    random.shuffle(l)
    count = 0
    loc = 0
    r = []
    while count < n:
        if len(l[loc]) > 65 and len(l[loc]) < 160:
            r.append(l[loc])
            count += 1
        loc += 1
    return r


def genQuoteLength(minlen, maxlen):
    l = open("quotes.txt", "r", encoding="utf-8").read().split("\n")
    random.shuffle(l)
    loc = 0
    while 1:
        if len(l[loc]) > minlen and len(l[loc]) < maxlen:
            return l[loc]
        loc += 1


def genSpanishQuote(minlen, maxlen):
    data = json.load(open("spanish.json", "r"))
    l = [p["Cita"] for p in data["quotes"]]
    random.shuffle(l)
    loc = 0
    while 1:
        if len(l[loc]) > minlen and len(l[loc]) < maxlen:
            return l[loc][1:-1]
        loc += 1


def gen_rand_mono_pair(quote, pat):
    key = key_s2tring_random(False)
    r = {chr(i + 65): key[i] for i in range(26)}
    plaintext = quote.upper()
    ciphertext = "".join(r.get(c, c) for c in plaintext)
    return ciphertext, plaintext


def gen_rand_affine_pair(quote):
    a = random.choice([3, 5, 7, 9, 11, 15, 17, 19, 21, 23])
    b = random.randint(3, 24)
    plaintext = quote.upper()
    ciphertext = ""
    for c in plaintext:
        if "A" <= c <= "Z":
            ciphertext += chr((a * (ord(c) - 65) + b) % 26 + 65)
        else:
            ciphertext += c
    return ciphertext, plaintext


def gen_rand_caesar_pair(quote):
    a = random.randint(3, 24)
    plaintext = quote.upper()
    ciphertext = ""
    for c in plaintext:
        if "A" <= c <= "Z":
            ciphertext += chr((ord(c) - 65 + a) % 26 + 65)
        else:
            ciphertext += c
    return ciphertext, plaintext


def gen_rand_vig_pair(quote):
    key = getRandWord(5, 8).upper()
    plaintext = quote.upper()
    ciphertext = ""
    for i, c in enumerate(plaintext):
        if "A" <= c <= "Z":
            k = key[i % len(key)]
            ciphertext += chr((ord(c) - 65 + ord(k) - 65) % 26 + 65)
        else:
            ciphertext += c
    return ciphertext, plaintext


def genRandPorta_pair(quote):
    key = getRandWord(5, 8).upper()
    plaintext = quote.upper()
    ciphertext = ""
    for i, c in enumerate(plaintext):
        if "A" <= c <= "Z":
            k = key[i % len(key)]
            x = ord(c) - 65
            y = ord(k) - 65
            if y % 2 == 1:
                y -= 1
            if x < 13:
                ciphertext += chr(((x + y) % 26) + 65)
            else:
                ciphertext += chr(((x - y) % 26) + 65)
        else:
            ciphertext += c
    return ciphertext, plaintext


def gen_rand_xeno_pair():
    key = key_s2tring_random(True)
    quote = genSpanishQuote(70, 160)
    r = {chr(i + 65): key[i] for i in range(14)}
    r["Ñ"] = key[14]
    for i in range(14, 26):
        r[chr(i + 65)] = key[i + 1]
    plaintext = quote.upper()
    ciphertext = "".join(r.get(c, c) for c in plaintext)
    return ciphertext, plaintext


def generate_test_pairs():
    l = [
        "1 2",
        "1 1",
        "1 0",
        "1 1",
        "2 1",
        "2 2",
        "2 1",
        "2 0",
        "4 D",
        "4 E",
        "4 D",
        "4 E",
        "5 C",
        "8 1",
        "8 1",
        "8 1",
    ]
    n = len(l)
    q = genQuotes(n + 1)
    pairs = []
    ct, pt = gen_rand_mono_pair(q[-1], False)
    pairs.append((ct, pt))
    for i in range(n):
        question = l[i].split(" ")
        if int(question[0]) <= 2:
            ct, pt = gen_rand_mono_pair(q[i], question[0] == "2")
        elif int(question[0]) == 4:
            ct, pt = gen_rand_caesar_pair(q[i])
        elif int(question[0]) == 8:
            ct, pt = gen_rand_xeno_pair()
        pairs.append((ct, pt))
    return pairs


def is_close(a, b):
    a = "".join(a.lower().split())
    b = "".join(b.lower().split())
    return a == b


def main():
    with open("./flag.txt", "r") as file:
        FLAG = file.read().strip()
    pairs = generate_test_pairs()
    sys.stdout.write("Welcome to the Codebusting Challenge!\n")
    sys.stdout.flush()
    start_time = time.time()
    for idx, (ct, pt) in enumerate(pairs):
        # sys.stdout.write(f"plaintext is {pt}\n")  # debugging purposes
        sys.stdout.write(f"Ciphertext {idx+1}: {ct}\nYour answer: ")
        sys.stdout.flush()
        user = sys.stdin.readline().strip()
        if time.time() - start_time > TIME_LIMIT:
            sys.stdout.write("Time limit exceeded.\n")
            sys.exit(1)
        if is_close(user, pt):
            continue
        else:
            sys.stdout.write("Incorrect.\n")
            sys.exit(1)
    sys.stdout.write(f"Congratulations! Here is your flag: {FLAG}\n")
    sys.exit(0)


if __name__ == "__main__":
    main()
