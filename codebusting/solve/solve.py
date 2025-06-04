from pwn import *
import time
from cryptogram_solver.sub_solver import *

def solve_cipher(ciphertext, cipher_type):
    solver = SubSolver(ciphertext, "./cryptogram_solver/english_corpus_generator/corpus.txt", False)
    solver.solve()
    return solver.print_report()

def main():
    # Connect to the server (correct port)
    conn = remote('localhost', 8148)
    log.info("Connected to server")
    
    # Receive welcome message
    welcome = conn.recvline().decode()
    log.info(f"Server says: {welcome}")
    
    # List of cipher types based on the challenge code
    cipher_types = [
        1,  # Initial monoalphabetic
        1, 1, 1, 1,  # More monoalphabetic
        2, 2, 2, 2,  # Similar monoalphabetic (with Ñ)
        4, 4, 4, 4,  # Caesar ciphers
        5,  # Placeholder/unknown
        8, 8, 8  # Spanish xenocrypt
    ]
    
    start_time = time.time()
    
    for i, cipher_type in enumerate(cipher_types):
        try:
            # Receive challenge
            conn.recvuntil(b"Ciphertext " + str(i+1).encode() + b": ")
            ciphertext_data = conn.recvuntil(b"Your answer: ")
            ciphertext = ciphertext_data.replace(b"Your answer: ", b"").decode().strip()
            
            log.info(f"Challenge {i+1}: {ciphertext[:30]}...")
            
            # Solve the cipher
            plaintext = solve_cipher(ciphertext, cipher_type)
            
            # Send solution
            conn.sendline(plaintext.encode())
            log.info(f"Sent solution: {plaintext[:30]}...")
            
            elapsed = time.time() - start_time
            log.info(f"Time elapsed: {elapsed:.2f}s / 10s")
            
        except Exception as e:
            log.error(f"Error in challenge {i+1}: {e}")
    
    # Get the flag
    flag = conn.recvline().decode().strip()
    log.success(f"Flag: {flag}")
    conn.close()

if __name__ == "__main__":
    main()
