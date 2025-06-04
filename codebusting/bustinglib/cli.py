from generator import *


def generate_question(question, i, q):
    if int(question[0]) <= 2:
        return gen_rand_mono(i, q[i], "1" if question[0] == "2" else 0, question[1])
    if int(question[0]) == 3:
        return gen_rand_affine(i, q[i], question[1])
    if int(question[0]) == 4:
        return gen_rand_caesar(i, q[i], question[1])
    if int(question[0]) == 5:
        return gen_rand_vig(i, q[i], question[1])
    if int(question[0]) == 8:
        return gen_rand_xeno(i, q[i], question[1])
    if int(question[0]) == 13:
        return genRandPorta(i, q[i], question[1])


def genTest():
    l = [
        "1 2",
        "1 1",
        "1 0",
        "1 1",
        "2 1",
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
        "8 1",
        "8 1",
        "13 E",
        "13 D",
        "13 C",
    ]

    n = len(l)

    q = genQuotes(n + 1)
    test = {"TEST.0": header(n, "BCACTF")}
    test["CIPHER.0"] = gen_rand_mono(0, q[len(q) - 1], False, 0)
    for i in range(n):
        question = l[i].split(" ")
        test["CIPHER." + str(i + 1)] = generate_question(question, i, q)
    
    print(json.dumps(test))
    return json.dumps(test)
    


if __name__ == "__main__":
    genTest()
