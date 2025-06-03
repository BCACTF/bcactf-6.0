import json
import random
import sympy


def header(n, name):
    return {
        "timed": 0,
        "count": n,
        "questions": list(range(1, n + 1)),
        "title": name + "",
        "useCustomHeader": False,
        "customHeader": "",
        "testtype": "cstate",
    }


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


def gen_rand_mono(num, quote, pat, hint):
    key = key_s2tring_random(False)
    r = {}
    for i in range(0, 26):
        r[chr(i + 65)] = key[i]
    x = {
        "cipherString": quote,
        "encodeType": "random",
        "offset": 1,
        "shift": 1,
        "offset2": 1,
        "keyword": "",
        "keyword2": "",
        "alphabetSource": "ABCDEFGHIJKLMNOPQRSTUVWXYZ",
        "alphabetDest": key,
        "curlang": "en",
        "replacement": r,
        "editEntry": str(num),
    }
    if pat == "1":
        x["cipherType"] = "patristocrat"
        x["question"] = "<p>Solve this patristocrat.</p>"
        x["points"] = 600
    else:
        x["cipherType"] = "aristocrat"
        x["question"] = "<p>Solve this aristocrat.</p>"
        x["points"] = 250
    if hint == "0":
        x["question"] = (
            x["question"][:-4] + " The first word is " + quote.split(" ")[0] + ".</p>"
        )
        if pat == "1":
            x["points"] = x["points"] - 30 * len(quote.split(" ")[0])
        else:
            x["points"] = x["points"] - 10 * len(quote.split(" ")[0])
    if hint == "1":
        letter = random.randint(97, 122)
        while r[chr(letter - 32)] not in quote.upper():
            letter = random.randint(97, 122)
        m = key[letter - 97]
        x["question"] = (
            x["question"][:-4]
            + " The letter "
            + chr(letter).upper()
            + " maps to "
            + m
            + ".</p>"
        )
        if pat == "1":
            x["points"] = x["points"] - 15 * quote.count(chr(letter))
        else:
            x["points"] = x["points"] - 5 * quote.count(chr(letter))
    return x


def gen_rand_xeno(num, quote, hint):
    key = key_s2tring_random(True)
    quote = genSpanishQuote(70, 160)
    r = {}
    for i in range(0, 14):
        r[chr(i + 65)] = key[i]
    r["Ñ"] = key[14]
    for i in range(14, 26):
        r[chr(i + 65)] = key[i + 1]
    x = {
        "cipherString": quote,
        "encodeType": "random",
        "offset": 1,
        "shift": 1,
        "offset2": 1,
        "keyword": "",
        "keyword2": "",
        "alphabetSource": "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ",
        "alphabetDest": key,
        "curlang": "es",
        "replacement": r,
        "editEntry": str(num),
        "cipherType": "aristocrat",
        "question": "<p>Solve this xenocrypt.</p>",
        "points": 400,
    }
    return x


def gen_rand_affine(num, quote, enc):
    a = random.choice([3, 5, 7, 9, 11, 15, 17, 19, 21, 23])
    b = random.randint(3, 24)
    r = {}
    for i in range(0, 26):
        r[str(i + 65)] = chr((i * a + b) % 26 + 65)
    x = {
        "a": a,
        "b": b,
        "cipherString": quote,
        "cipherType": "affine",
        "solclick1": -1,
        "solclick2": -1,
        "replacement": r,
        "curlang": "en",
        "editEntry": num,
    }
    if enc == "E":
        x["operation"] = "encode"
        x["points"] = 175
        x["question"] = (
            "<p>Encode this sentence with the Affine cipher. (a,b)=("
            + str(a)
            + ","
            + str(b)
            + ").</p>"
        )
    elif enc == "D":
        x["operation"] = "decode"
        x["points"] = 150
        x["question"] = (
            "<p>Decode this sentence which has been encoded with an Affine cipher. (a,b)=("
            + str(a)
            + ","
            + str(b)
            + ").</p>"
        )
    elif enc == "C":
        one = random.randint(0, 12)
        two = random.randint(13, 25)
        onemap = (one * a + b) % 26
        twomap = (two * a + b) % 26
        x["operation"] = "crypt"
        x["points"] = 200
        x["question"] = (
            "<p>Decode this sentence which has been encoded with an Affine cipher. The letters "
            + chr(onemap + 65)
            + " and "
            + chr(twomap + 65)
            + " map to "
            + chr(one + 65)
            + " and "
            + chr(two + 65)
            + ".</p>"
        )
    return x


def gen_rand_caesar(num, quote, enc):
    a = random.randint(3, 24)
    r = {}
    for i in range(0, 26):
        r[str(i + 65)] = chr((i + a) % 26 + 65)
    x = {
        "offset": a,
        "offset2": None,
        "cipherString": quote,
        "cipherType": "caesar",
        "solclick1": -1,
        "solclick2": -1,
        "replacement": r,
        "curlang": "en",
        "editEntry": num,
        "shift": None,
    }
    if enc == "E":
        x["operation"] = "encode"
        x["points"] = 150
        x["question"] = (
            "<p>Encode this sentence with the Caesar cipher with offset "
            + str(a)
            + ".</p>"
        )
    elif enc == "D":
        x["operation"] = "decode"
        x["points"] = 125
        x["question"] = (
            "<p>Decode this sentence which has been encoded with an Caesar cipher.</p>"
        )
    return x


def gen_rand_vig(num, quote, enc):
    quote = genQuoteLength(50, 70)
    key = getRandWord(5, 8)
    x = {
        "cipherType": "vigenere",
        "keyword": key,
        "cipherString": quote,
        "findString": "",
        "blocksize": len(key),
        "curlang": "en",
        "editEntry": str(num),
    }
    if enc == "E":
        x["operation"] = "encode"
        x["question"] = (
            "<p>Encode this sentence with the Vigenere cipher using the keyword "
            + key
            + ".</p>"
        )
        x["points"] = "200"
    if enc == "D":
        x["operation"] = "decode"
        x["question"] = (
            "<p>Decode this sentence with the Vigenere cipher using the keyword "
            + key
            + ".</p>"
        )
        x["points"] = "175"
    if enc == "C":
        x["operation"] = "crypt"
        x["question"] = (
            "<p>Decode this sentence with the Vigenere cipher. The first "
            + str(len(key))
            + " characters of the sentence is "
            + quote[: len(key)]
            + ".</p>"
        )
        x["points"] = "175"
    return x


def genRandPorta(num, quote, enc):
    quote = genQuoteLength(50, 70)
    key = getRandWord(5, 8)
    x = {
        "cipherType": "porta",
        "keyword": key,
        "cipherString": quote,
        "findString": "",
        "blocksize": len(key),
        "curlang": "en",
        "editEntry": str(num),
    }
    if enc == "E":
        x["operation"] = "encode"
        x["question"] = (
            "<p>Encode this sentence with the Porta cipher using the keyword "
            + key
            + ".</p>"
        )
        x["points"] = "200"
    if enc == "D":
        x["operation"] = "decode"
        x["question"] = (
            "<p>Decode this sentence with the Porta cipher using the keyword "
            + key
            + ".</p>"
        )
        x["points"] = "175"
    if enc == "C":
        x["operation"] = "crypt"
        x["question"] = (
            "<p>Decode this sentence with the Porta cipher. The first "
            + str(len(key))
            + " characters of the sentence is "
            + quote[: len(key)]
            + ".</p>"
        )
        x["points"] = "175"
    return x


def getRandWord(min, max):
    f = open("words.txt", "r")
    for i in range(random.randint(0, 9000)):
        f.readline()
    r = ""
    while len(r) < min or len(r) > max:
        r = f.readline().strip()
    return r


def genQuotes(n):
    # quotes = open("quotes.txt", "r")
    l = open("quotes.txt", "r", encoding="utf-8").read().split("\n")
    # for i in range(40569):
    #     l.append(quotes.readline().strip())
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


def genQuoteLength(min, max):
    # quotes = open("quotes.txt", "r")
    l = open("quotes.txt", "r", encoding="utf-8").read().split("\n")
    # for i in range(40569):
    #     l.append(quotes.readline().strip())
    random.shuffle(l)
    loc = 0
    while 1:
        if len(l[loc]) > min and len(l[loc]) < max:
            return l[loc]
        loc += 1


def genSpanishQuote(min, max):
    json_file = open("spanish.json", "r", encoding="mbcs")
    data = json.load(json_file)
    l = []
    for p in data["quotes"]:
        l.append(p["Cita"])
    random.shuffle(l)
    loc = 0
    while 1:
        if len(l[loc]) > min and len(l[loc]) < max:
            q = l[loc][1:-1]
            return q
        loc += 1
