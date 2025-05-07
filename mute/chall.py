blacklist = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

# Only allow symbols, but check for too many underscores
def security_check(s):
    return any(c in blacklist for c in s) or s.count('_') > 50

# Fixed small buffer
BUFFER_SIZE = 32

while True:
    cmds = input("> ")
    
    # simulate a small fixed-size buffer

    if security_check(cmds):
        print("invalid input")
    else:
        if len(cmds) > BUFFER_SIZE:
            print("bcactf{this_is_a_flag}")
            break
        else:
            print("nope")