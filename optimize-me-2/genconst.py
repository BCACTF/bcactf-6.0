#!/usr/bin/env python3
import sys
import math


def fibonacci_modular_fast(n, mod=256):
    """
    Calculate fibonacci(n) % mod using matrix exponentiation
    Memory: O(log n), Time: O(log n), but still CPU intensive for large n
    """
    if n <= 1:
        return n % mod

    def matrix_mult_mod(A, B, mod):
        return [
            [
                (A[0][0] * B[0][0] + A[0][1] * B[1][0]) % mod,
                (A[0][0] * B[0][1] + A[0][1] * B[1][1]) % mod,
            ],
            [
                (A[1][0] * B[0][0] + A[1][1] * B[1][0]) % mod,
                (A[1][0] * B[0][1] + A[1][1] * B[1][1]) % mod,
            ],
        ]

    def matrix_power_mod(matrix, power, mod):
        if power == 1:
            return [
                [matrix[0][0] % mod, matrix[0][1] % mod],
                [matrix[1][0] % mod, matrix[1][1] % mod],
            ]

        if power % 2 == 0:
            half = matrix_power_mod(matrix, power // 2, mod)
            return matrix_mult_mod(half, half, mod)
        else:
            return matrix_mult_mod(
                matrix, matrix_power_mod(matrix, power - 1, mod), mod
            )

    # Fibonacci matrix [[1,1],[1,0]]
    fib_matrix = [[1, 1], [1, 0]]
    result_matrix = matrix_power_mod(fib_matrix, n, mod)
    return result_matrix[0][1]


def simple_sieve(limit):
    """Basic sieve for finding primes up to limit"""
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False

    for i in range(2, int(math.sqrt(limit)) + 1):
        if is_prime[i]:
            for j in range(i * i, limit + 1, i):
                is_prime[j] = False

    return [i for i in range(2, limit + 1) if is_prime[i]]


def get_nth_prime_direct(n):
    """
    Find nth prime by generating primes directly - more reliable
    """
    if n <= 0:
        raise ValueError("n must be positive")

    # Handle small cases with known primes
    if n <= 25:
        small_primes = [
            2,
            3,
            5,
            7,
            11,
            13,
            17,
            19,
            23,
            29,
            31,
            37,
            41,
            43,
            47,
            53,
            59,
            61,
            67,
            71,
            73,
            79,
            83,
            89,
            97,
        ]
        return small_primes[n - 1]

    # For larger n, use a more conservative upper bound
    # Upper bound formula: p_n < n * ln(n) + n * ln(ln(n)) for n >= 6
    ln_n = math.log(n)
    if n >= 6:
        upper_bound = int(n * (ln_n + math.log(ln_n)) * 1.2)  # 20% safety margin
    else:
        upper_bound = 30

    # Make sure upper bound is reasonable
    upper_bound = max(upper_bound, n * 15)

    # print(
    #     f"  Generating primes up to {upper_bound} to find prime #{n}...",
    #     file=sys.stderr,
    # )

    # Generate all primes up to the upper bound
    primes = simple_sieve(upper_bound)

    if len(primes) >= n:
        return primes[n - 1]
    else:
        # If we still don't have enough primes, expand the search
        # print(f"  Need more primes, expanding search...", file=sys.stderr)
        upper_bound *= 2
        primes = simple_sieve(upper_bound)

        if len(primes) >= n:
            return primes[n - 1]
        else:
            raise RuntimeError(
                f"Could not find prime #{n} even with upper bound {upper_bound}"
            )


def generate_flag_constants(flag):
    """
    Generate constants using fibonacci and prime computations only
    """
    flag_bytes = flag.encode("utf-8")

    print("// Generated constants for computationally expensive flag decryption")
    print("// Flag must be decrypted using fibonacci and prime computations")
    print("// Using high-CPU, low-memory algorithms")
    print()

    # More reasonable constants that are still very expensive with naive methods
    # but manageable for generation
    fib_base = 10000  # F(1M) - still very expensive with recursive method
    prime_start = 500000  # 50,000th prime - expensive but manageable

    print("const int fibonacci_base = {};".format(fib_base))
    print("const int prime_start_index = {};".format(prime_start))
    print()

    print("const unsigned char encrypted_flag[] = {", end="")

    for i, byte in enumerate(flag_bytes):
        # print(
        #     f"\nProcessing character {i+1}/{len(flag_bytes)}: '{chr(byte)}'",
        #     file=sys.stderr,
        # )

        # Fibonacci using matrix exponentiation (CPU intensive but low memory)
        # print(
        #     f"  Computing F({fib_base + i}) mod 256 using matrix exponentiation...",
        #     file=sys.stderr,
        # )
        fib_key = fibonacci_modular_fast(fib_base + i, 256)
        # print(f"    Fibonacci key: {fib_key}", file=sys.stderr)

        # Prime using direct sieve generation
        # print(f"  Finding prime #{prime_start + i}...", file=sys.stderr)
        prime_val = get_nth_prime_direct(prime_start + i)
        prime_key = prime_val % 256
        # print(
        #     f"    Prime #{prime_start + i} = {prime_val}, key = {prime_key}",
        #     file=sys.stderr,
        # )

        # Combine both keys using XOR
        combined_key = fib_key ^ prime_key
        encrypted = byte ^ combined_key

        # print(
        #     f"  Keys: fib={fib_key}, prime={prime_key}, combined={combined_key}",
        #     file=sys.stderr,
        # )

        if i > 0:
            print(",", end="")
        print(f" 0x{encrypted:02x}", end="")

    print(" };")
    print()
    print(f"const int flag_length = {len(flag_bytes)};")
    print()

    print(f"// Original flag: {flag}")
    print("// Each byte encrypted with: byte XOR fib_key XOR prime_key")
    print(
        "// These constants will take a VERY LONG TIME to compute with naive algorithms:"
    )
    print(
        f"// - Fibonacci F({fib_base}) to F({fib_base + len(flag_bytes) - 1}) using recursive method"
    )
    print(
        f"// - Primes #{prime_start} to #{prime_start + len(flag_bytes) - 1} using trial division"
    )

    return flag


if __name__ == "__main__":
    if len(sys.argv) > 1:
        flag = sys.argv[1]
    else:
        flag = "bcactf{sl0w_m4th_f4st_c0d3}"

    print(f"Generating constants for flag: {flag}", file=sys.stderr)
    print("Using CPU-intensive but memory-efficient algorithms...", file=sys.stderr)

    generate_flag_constants(flag)

    print("Generation complete!", file=sys.stderr)
