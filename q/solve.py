from pwn import *
from json import loads

while True:
    conn = remote('challs.bcactf.com', 32783)

    it = conn.recvuntil(b'What is the secret? ')
    lines = [loads(ln) for ln in it.splitlines()[0:-1]]

    mins = [math.inf for _ in lines[0]]

    for ln in lines:
        for i in range(len(ln)):
            mins[i] = min(mins[i], ln[i])
    good = ''.join(map(chr,mins))

    conn.sendline(good.encode())
    res = conn.recvline()
    if b'Wrong ' in res:
        continue

    print('DONE')
    print(res)
    print(conn.recvline())
    break
