from generator import *


def generate_all_types_exam() -> list:
    l = [
        "1 2",
        "1 1",
        "1 0",
        "2 2",
        "2 1",
        "2 0",
        "3 D",
        "3 E",
        "3 C",
        "4 D",
        "4 E",
        "5 D",
        "5 E",
        "5 C",
        "6 D",
        "6 E",
        "6 C",
        "7 D",
        "7 E",
        "8 1",
        "9 L",
        "9 S",
        "9 W",
        "11 D",
        "11 C",
        "12 D",
        "12 C",
        "13 E",
        "13 D",
        "13 C",
        "14 2",
        "14 4",
        "14 R",
    ]
    return l


def generate_national_exam() -> list:
    aff = ["3 D", "3 E", "3 C"]
    vig = ["5 D", "5 E", "5 C"]
    hill2 = ["6 D", "6 E", "6 C"]
    hill3 = ["7 D", "7 E"]
    bac = ["9 L", "9 S", "9 W"]
    mor = ["11 D", "11 C", "12 D", "12 C"]
    random.shuffle(aff)
    random.shuffle(vig)
    random.shuffle(hill2)
    random.shuffle(hill3)
    random.shuffle(bac)
    random.shuffle(mor)
    l = [
        "1 2",
        "1 2",
        "1 2",
        "1 2",
        "1 2",
        "1 2",
        "1 2",
        "1 2",
        "1 2",
        "1 2",
        "2 2",
        "2 1",
        "2 0",
        aff[0],
        aff[1],
        "4 D",
        "4 E",
        vig[0],
        vig[1],
        hill2[0],
        hill2[1],
        hill3[0],
        "8 1",
        bac[0],
        bac[1],
        "10 D",
        "10 E",
        mor[0],
        mor[1],
        mor[2],
    ]
    return l


def generate_regional_exam() -> list:
    enc = ["3 E", "4 E", "5 E", "6 E"]
    bac = ["9 L", "9 S", "9 W"]
    random.shuffle(enc)
    random.shuffle(bac)
    l = [
        "1 0",
        "1 1",
        "1 2",
        "1 2",
        "1 2",
        "1 2",
        "2 2",
        "2 0",
        "3 D",
        "4 D",
        "5 D",
        "6 D",
        enc[0],
        enc[1],
        "8 1",
        bac[0],
        bac[1],
        "11 D",
        "12 D",
    ]
    return l


def generate_aristo_spam() -> list:
    n = int(input("How many aristos? "))
    l = ["1 2"] * n
    return l


def generate_patristo_spam() -> list:
    n = int(input("How many patristos? "))
    l = ["2 2"] * n
    return l


def generate_question(question, i, q):
    if int(question[0]) <= 2:
        return gen_rand_mono(i, q[i], "1" if question[0] == "2" else 0, question[1])
    if int(question[0]) == 3:
        return gen_rand_affine(i, q[i], question[1])
    if int(question[0]) == 4:
        return gen_rand_caesar(i, q[i], question[1])
    if int(question[0]) == 5:
        return gen_rand_vig(i, q[i], question[1])
    if int(question[0]) == 6:
        return genRand2x2Hill(i, q[i], question[1])
    if int(question[0]) == 7:
        return genRand3x3Hill(i, q[i], question[1])
    if int(question[0]) == 8:
        return gen_rand_xeno(i, q[i], question[1])
    if int(question[0]) == 9:
        return genRandBacon(i, q[i], question[1])
    if int(question[0]) == 10:
        return RSA(i, question[1])
    if int(question[0]) == 11:
        return genRandMorbit(i, q[i], question[1])
    if int(question[0]) == 12:
        return genRandPollux(i, q[i], question[1])
    if int(question[0]) == 13:
        return genRandPorta(i, q[i], question[1])
    if int(question[0]) == 14:
        return genRandRailFence(i, q[i], question[1])


def genTest():
    na = input("Test Name: ")
    preset = input(
        "Would you like to use a preset? 1 = All types, 2 = National level test, 3 = Regional level test, 4 = Aristo Spam, 5 = Patristo Spam"
    )
    l = []
    if preset == "1":
        l = generate_all_types_exam()
    elif preset == "2":
        l = generate_national_exam()
    elif preset == "3":
        l = generate_regional_exam()
    elif preset == "4":
        l = generate_aristo_spam()
    elif preset == "5":
        l = generate_patristo_spam()

    n = len(l)

    q = genQuotes(n + 1)
    test = {"TEST.0": header(n, na)}
    test["CIPHER.0"] = gen_rand_mono(0, q[len(q) - 1], False, 0)
    for i in range(n):
        question = l[i].split(" ")
        test["CIPHER." + str(i + 1)] = generate_question(question, i, q)

    with open("CodeTests/" + na + ".json", "w") as file:
        file.write(json.dumps(test))
        file.close()
    return json.dumps(test)


if __name__ == "__main__":
    genTest()
