import subprocess
import sys

i=0
while True:
    i += 1
    proc = subprocess.run(
        ['./math'],
        input=str(i) + '\n',
        capture_output=True,
        text=True
    )
    output = proc.stdout.strip()
    if output == "A+":
        print(f'--------{i}')
    else:
        print(i)

    if i>10**10:
        sys.exit(0)
