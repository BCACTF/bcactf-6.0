#!/usr/bin/env python3
import hashlib
import sys
from functools import lru_cache

# Global memoization caches
_fib_cache = {}
_prime_cache = []
_hash_cache = {}


def fibonacci_iterative_memoized(n):
    """Calculate fibonacci number with memoization"""
    if n in _fib_cache:
        return _fib_cache[n]

    if n <= 1:
        _fib_cache[n] = n
        return n

    # Find the highest cached value to start from
    start = 0
    a, b = 0, 1

    # Check if we have any cached values to start from
    for cached_n in sorted(_fib_cache.keys()):
        if cached_n < n:
            start = cached_n
            if cached_n == 0:
                a = 0
            elif cached_n == 1:
                b = 1
            else:
                a = _fib_cache[cached_n - 1] if cached_n - 1 in _fib_cache else a
                b = _fib_cache[cached_n]

    # Calculate from start to n, caching intermediate results
    for i in range(max(2, start + 1), n + 1):
        temp = a + b
        _fib_cache[i] = temp
        a, b = b, temp

    return _fib_cache[n]


@lru_cache(maxsize=1000000)
def is_prime_cached(n):
    """Check if number is prime with caching"""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    # Use 6k±1 optimization for better performance
    if n == 3:
        return True
    if n % 3 == 0:
        return False

    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6

    return True


def sieve_of_eratosthenes(limit):
    """Generate primes up to limit using Sieve of Eratosthenes"""
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False

    for i in range(2, int(limit**0.5) + 1):
        if is_prime[i]:
            for j in range(i * i, limit + 1, i):
                is_prime[j] = False

    return [i for i in range(2, limit + 1) if is_prime[i]]


def get_nth_prime_optimized(n):
    """Get the nth prime number with optimized algorithms"""
    global _prime_cache

    # If we already have enough primes cached, return from cache
    if len(_prime_cache) >= n:
        return _prime_cache[n - 1]

    # Estimate upper bound for nth prime using prime number theorem
    if n >= 6:
        # Approximation: p_n ≈ n * ln(n) + n * ln(ln(n))
        import math

        ln_n = math.log(n)
        upper_bound = int(n * (ln_n + math.log(ln_n) - 1 + 1.8 * math.log(ln_n) / ln_n))
        upper_bound = max(upper_bound, n * 15)  # Safety margin
    else:
        upper_bound = 30

    # If we need a lot of primes, use sieve
    if n > 1000 and len(_prime_cache) < n // 2:
        print(f"Using sieve to generate primes up to {upper_bound}...", file=sys.stderr)
        _prime_cache = sieve_of_eratosthenes(upper_bound)
        if len(_prime_cache) >= n:
            return _prime_cache[n - 1]

    # Fill cache incrementally if sieve wasn't enough
    candidate = _prime_cache[-1] + 1 if _prime_cache else 2

    while len(_prime_cache) < n:
        if is_prime_cached(candidate):
            _prime_cache.append(candidate)
        candidate += 1

        # Progress indicator for large computations
        if len(_prime_cache) % 10000 == 0:
            print(f"Found {len(_prime_cache)} primes...", file=sys.stderr)

    return _prime_cache[n - 1]


def compute_hash_chain_cached(seed, position, iterations):
    """Compute hash chain with caching"""
    cache_key = (seed, position, iterations)

    if cache_key in _hash_cache:
        return _hash_cache[cache_key]

    input_str = f"{seed}{position}"
    current_hash = input_str.encode()

    # Use SHA256 directly for better performance
    for _ in range(iterations):
        current_hash = hashlib.sha256(current_hash).digest()

    result = current_hash[0]
    _hash_cache[cache_key] = result
    return result


def generate_flag_constants(flag):
    """
    Generate constants for a flag where decryption requires all three expensive computations
    """
    flag_bytes = flag.encode("utf-8")

    print("// Generated constants for computationally expensive flag decryption")
    print(
        "// Flag must be decrypted using ALL THREE mathematical computations combined"
    )
    print()

    # We'll use all three methods together to encrypt each byte
    fib_base = 1000000
    prime_start = 1000000
    hash_iterations = 500000
    hash_seed = "CTF_SEED_2023"

    print("const int fibonacci_base = {};".format(fib_base))
    print("const int prime_start_index = {};".format(prime_start))
    print(f"const int hash_iterations = {hash_iterations};")
    print(f'const char hash_seed[] = "{hash_seed}";')
    print()

    # Pre-compute some primes if we need many
    max_prime_needed = prime_start + len(flag_bytes)
    print(f"Pre-computing primes up to #{max_prime_needed}...", file=sys.stderr)

    # Encrypt each byte using combination of all three methods
    print("const unsigned char encrypted_flag[] = {", end="")

    for i, byte in enumerate(flag_bytes):
        print(
            f"Processing character {i+1}/{len(flag_bytes)}: '{chr(byte)}'",
            file=sys.stderr,
        )

        # Get keys from all three methods
        print(f"  Computing fibonacci({fib_base + i})...", file=sys.stderr)
        fib_key = fibonacci_iterative_memoized(fib_base + i) % 256

        print(f"  Finding prime #{prime_start + i}...", file=sys.stderr)
        prime_key = get_nth_prime_optimized(prime_start + i) % 256

        print(
            f"  Computing hash chain with {hash_iterations} iterations...",
            file=sys.stderr,
        )
        hash_key = compute_hash_chain_cached(hash_seed, i, hash_iterations)

        # Combine all three keys using XOR
        combined_key = fib_key ^ prime_key ^ hash_key
        encrypted = byte ^ combined_key

        if i > 0:
            print(",", end="")
        print(f" 0x{encrypted:02x}", end="")

    print(" };")
    print()
    print(f"const int flag_length = {len(flag_bytes)};")
    print()

    # Verification info
    print(f"// Original flag: {flag}")
    print("// Each byte encrypted with: byte XOR fib_key XOR prime_key XOR hash_key")

    # Print some debug info
    print(f"// Fibonacci cache size: {len(_fib_cache)}", file=sys.stderr)
    print(f"// Prime cache size: {len(_prime_cache)}", file=sys.stderr)
    print(f"// Hash cache size: {len(_hash_cache)}", file=sys.stderr)

    return flag


# For backwards compatibility, keep the old function names as aliases
def fibonacci_iterative(n):
    return fibonacci_iterative_memoized(n)


def is_prime(n):
    return is_prime_cached(n)


def get_nth_prime(n):
    return get_nth_prime_optimized(n)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        flag = sys.argv[1]
    else:
        flag = "bcactf{sl0w_m4th_f4st_c0d3}"

    print(f"Generating constants for flag: {flag}", file=sys.stderr)
    print(f"This may take a while for large constants...", file=sys.stderr)

    generate_flag_constants(flag)

    print("Generation complete!", file=sys.stderr)
