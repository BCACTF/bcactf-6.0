import pwn

# Connect to localhost:8080
conn = pwn.remote('localhost', 8080)

# Open solve.txt and send each line
with open('solve.txt', 'r') as f:
    for line in f.read().splitlines():
        if line.strip() == '' or line.startswith(";"):
            continue
        # print("sending line: ", line.rstrip('\n'))
        conn.sendline(line.rstrip('\n').encode('utf-8'))
        response = conn.recvline()
        print(response.decode('utf-8', errors='ignore').rstrip())



conn.close()