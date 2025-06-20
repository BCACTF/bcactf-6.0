#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <openssl/sha.h>

// Generated constants for computationally expensive flag decryption
// Flag must be decrypted using ALL THREE mathematical computations combined

const int fibonacci_base = 20;
const int prime_start_index = 50;
const int hash_iterations = 50000;
const char hash_seed[] = "CTF_SEED_2023";

const unsigned char encrypted_flag[] = { 0x6f, 0x38, 0x1f, 0x48, 0x97, 0xd8, 0x7f, 0x3c, 0x29, 0x84, 0x0f, 0x7a, 0x51, 0x28, 0x65, 0xa6, 0xf3, 0x10, 0x67, 0xde, 0x85, 0x2c, 0x73 };

const int flag_length = 23;

// SLOW: Recursive fibonacci (exponential time complexity)
long long fibonacci_recursive_slow(int n) {
    if (n <= 1) return n;
    return fibonacci_recursive_slow(n - 1) + fibonacci_recursive_slow(n - 2);
}

// FAST: Iterative fibonacci (linear time complexity)
long long fibonacci_iterative_fast(int n) {
    if (n <= 1) return n;
    long long a = 0, b = 1;
    for (int i = 2; i <= n; i++) {
        long long temp = a + b;
        a = b;
        b = temp;
    }
    return b;
}

// SLOW: Naive prime checking (check all numbers up to n-1)
int is_prime_slow(long long n) {
    if (n < 2) return 0;
    for (long long i = 2; i < n; i++) {
        if (n % i == 0) return 0;
    }
    return 1;
}

// FAST: Optimized prime checking (check only up to sqrt(n))
int is_prime_fast(long long n) {
    if (n < 2) return 0;
    if (n == 2) return 1;
    if (n % 2 == 0) return 0;
    
    for (long long i = 3; i * i <= n; i += 2) {
        if (n % i == 0) return 0;
    }
    return 1;
}

// SLOW: Find nth prime using slow prime checking
long long get_nth_prime_slow(int n) {
    int count = 0;
    long long candidate = 2;
    
    while (count < n) {
        if (is_prime_slow(candidate)) {
            count++;
            if (count == n) return candidate;
        }
        candidate++;
    }
    return candidate;
}

// FAST: Find nth prime using fast prime checking
long long get_nth_prime_fast(int n) {
    int count = 0;
    long long candidate = 2;
    
    while (count < n) {
        if (is_prime_fast(candidate)) {
            count++;
            if (count == n) return candidate;
        }
        candidate++;
    }
    return candidate;
}

// Hash chain computation
void compute_hash_chain(const char* seed, int position, int iterations, unsigned char* result) {
    char input[256];
    snprintf(input, sizeof(input), "%s%d", seed, position);
    
    unsigned char hash[SHA256_DIGEST_LENGTH];
    SHA256_CTX ctx;
    
    // Initial hash
    SHA256_Init(&ctx);
    SHA256_Update(&ctx, input, strlen(input));
    SHA256_Final(hash, &ctx);
    
    // Iterate hash chain
    for (int i = 0; i < iterations; i++) {
        SHA256_Init(&ctx);
        SHA256_Update(&ctx, hash, SHA256_DIGEST_LENGTH);
        SHA256_Final(hash, &ctx);
    }
    
    *result = hash[0];  // Use first byte as key
}

// Decrypt flag using all three methods combined
void decrypt_flag(char* result) {
    printf("Starting combined mathematical decryption...\n");
    printf("Each character requires fibonacci + prime + hash computations.\n\n");
    
    for (int i = 0; i < flag_length; i++) {
        printf("Decrypting character %d/%d:\n", i + 1, flag_length);
        
        // Step 1: Compute fibonacci number
        printf("  Computing F(%d)... ", fibonacci_base + i);
        fflush(stdout);
        // Use SLOW recursive fibonacci - major bottleneck!
        long long fib = fibonacci_recursive_slow(fibonacci_base + i);
        unsigned char fib_key = fib % 256;
        printf("F(%d) = %lld (key: 0x%02x)\n", fibonacci_base + i, fib, fib_key);
        
        // Step 2: Find nth prime
        printf("  Finding prime #%d... ", prime_start_index + i);
        fflush(stdout);
        // Use SLOW prime finding - another bottleneck!
        long long prime = get_nth_prime_slow(prime_start_index + i);
        unsigned char prime_key = prime % 256;
        printf("Prime #%d = %lld (key: 0x%02x)\n", prime_start_index + i, prime, prime_key);
        
        // Step 3: Compute hash chain
        printf("  Computing hash chain (%d iterations)... ", hash_iterations);
        fflush(stdout);
        unsigned char hash_key;
        compute_hash_chain(hash_seed, i, hash_iterations, &hash_key);
        printf("Hash key: 0x%02x\n", hash_key);
        
        // Step 4: Combine all keys and decrypt
        unsigned char combined_key = fib_key ^ prime_key ^ hash_key;
        result[i] = encrypted_flag[i] ^ combined_key;
        
        printf("  Combined key: 0x%02x ^ 0x%02x ^ 0x%02x = 0x%02x\n", 
               fib_key, prime_key, hash_key, combined_key);
        printf("  Decrypted: '%c'\n\n", result[i]);
    }
    
    result[flag_length] = '\0';
}

void print_separator(char c, int length) {
    for (int i = 0; i < length; i++) {
        putchar(c);
    }
    putchar('\n');
}

int main() {
    printf("CTF Challenge: Combined Mathematical Optimization\n");
    print_separator('=', 50);
    printf("\n");
    printf("This program decrypts a flag using THREE expensive mathematical computations:\n");
    printf("1. Recursive Fibonacci calculation (exponential time)\n");
    printf("2. Naive prime number finding (very slow for large primes)\n");
    printf("3. Iterative SHA256 hash chains (computationally expensive)\n\n");
    printf("Each character of the flag requires ALL THREE computations!\n");
    printf("Your goal: Optimize ALL the algorithms to get the flag faster!\n\n");
    
    char* flag = malloc(flag_length + 1);
    if (!flag) {
        printf("Memory allocation failed!\n");
        return 1;
    }
    
    printf("Expected optimizations:\n");
    printf("- Replace recursive fibonacci with iterative version\n");
    printf("- Use sqrt(n) limit for prime checking instead of checking all numbers\n");
    printf("- Potentially cache/memoize repeated calculations\n\n");
    
    printf("Starting decryption (this will be VERY slow without optimization)...\n");
    print_separator('-', 50);
    
    decrypt_flag(flag);
    
    print_separator('=', 50);
    printf("DECRYPTION COMPLETE!\n");
    printf("FLAG: %s\n", flag);
    print_separator('=', 50);
    
    free(flag);
    return 0;
}
