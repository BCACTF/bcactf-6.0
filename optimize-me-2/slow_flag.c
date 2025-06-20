#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>

const int fibonacci_base = 10000;
const int prime_start_index = 500000;

const unsigned char encrypted_flag[] = { 0xea, 0x09, 0x12, 0x47, 0x98, 0x2d, 0xdb, 0x17, 0xd5, 0xbe, 0xe3, 0xde, 0xcf, 0x62, 0xb3, 0xb2, 0x73, 0xaf, 0xe6, 0xe1, 0xb5, 0x5f, 0xc3, 0x19, 0x0e, 0xfd, 0xe2 };

const int flag_length = 27;

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
        candidate += (candidate > 2) ? 2 : 1;  // Skip even numbers after 2
    }
    return candidate;
}

// Decrypt flag using both fibonacci and prime computations
void decrypt_flag(char* result) {
    for (int i = 0; i < flag_length; i++) {
        // Step 1: Compute fibonacci number
        // Use SLOW recursive fibonacci - major bottleneck!
        long long fib = fibonacci_recursive_slow(fibonacci_base + i);
        unsigned char fib_key = fib % 256;
        
        // Step 2: Find nth prime
        // Use SLOW prime finding - another bottleneck!
        long long prime = get_nth_prime_slow(prime_start_index + i);
        unsigned char prime_key = prime % 256;
        
        // Step 3: Combine keys and decrypt
        unsigned char combined_key = fib_key ^ prime_key;
        result[i] = encrypted_flag[i] ^ combined_key;

    }
    
    result[flag_length] = '\0';
}


int main() {
    char* flag = malloc(flag_length + 1);
    if (!flag) {
        printf("Memory allocation failed!\n");
        return 1;
    }
    
    decrypt_flag(flag);
    printf("DECRYPTION COMPLETE!\n");
    printf("FLAG: %s\n", flag);
    
    free(flag);
    return 0;
}
