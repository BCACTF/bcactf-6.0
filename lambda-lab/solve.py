import pwn

# Connect to localhost:8080
conn = pwn.remote('localhost', 8080)

# Open solve.txt and send each line
with open('solve.txt', 'r') as f:
    for line in f.read().splitlines():
        conn.sendline(line.rstrip('\n').encode('utf-8'))
        response = conn.recvline()
        print(response.decode('utf-8', errors='ignore').rstrip())



conn.close()