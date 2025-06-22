import math
from Crypto.Util.number import getPrime
from random import randint

def get_upper_bound_of_d(n, no_of_primes):
    for _ in range(no_of_primes):
        n = math.isqrt(n)
    return n // 3

def create_keys(pub_key_size=2048, no_of_primes=8):
    primes_arr = [getPrime(pub_key_size//no_of_primes) for i in range(no_of_primes)]
    N = math.prod(primes_arr)
    phi_N = math.prod([a - 1 for a in primes_arr])
    upper_bound = get_upper_bound_of_d(N, no_of_primes)
    while True:
        d = randint(2, upper_bound)
        try:
            e = pow(d, -1, phi_N)
        except:
            continue
        if (e * d) % phi_N == 1:
            return primes_arr, N, d, e

def main():
    primes_arr, N, d, e = create_keys()
    flag = "bcactf{WIENeR$-@7t4ck-$t1L1-w0rkS}"
    flag_int = int.from_bytes(flag.encode())
    ctext = pow(flag_int, e, N)
    print(f"ciphertext = {ctext}\ne = {e}\nN = {N}")
    ptext = pow(ctext, d, N)
    print(f"plaintext = {int.to_bytes(pow(ctext, d, N), math.ceil(ptext.bit_length()/8))}")

if __name__ == "__main__":
    main()