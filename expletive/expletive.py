blacklist = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

def security_check(s):
    return any(c in blacklist for c in s) or s.count('_') > 50

BUFFER_SIZE = 36

while True:
    cmds = input("> ")

    if security_check(cmds):
        print("invalid input")
    else:
        if len(cmds) > BUFFER_SIZE:
            print("bcactf{fudG3_5hOo7_d4rn100}")
            break
        else:
            print("nope")