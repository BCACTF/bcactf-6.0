#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <math.h>

// Generated encrypted flag constants
const unsigned char encrypted_flag[] = { 0x77, 0x62, 0x61, 0x32, 0x78, 0x6d, 0x74, 0x1b, 0x35, 0x53, 0x26, 0x04, 0x6c, 0x5e, 0x01, 0x1b, 0x70, 0x42, 0x30, 0x0c, 0x63, 0x4e, 0x1a, 0x19, 0x33, 0x46, 0x27, 0x51 };
const int flag_length = 28;

// Key derivation constants
const int key_multiplier = 37;
const int key_offset = 42;

// Intentionally slow fibonacci calculation (obvious optimization target)
long long slow_fibonacci(int n) {
    if (n <= 1) return n;
    return slow_fibonacci(n - 1) + slow_fibonacci(n - 2);
}

// Intentionally slow prime checking (another obvious target)
int is_prime_slow(long long n) {
    if (n < 2) return 0;
    for (long long i = 2; i < n; i++) {  // Intentionally checking all numbers
        if (n % i == 0) return 0;
    }
    return 1;
}

// Complex mathematical transformation for flag decryption
unsigned char complex_decrypt_byte(unsigned char encrypted_byte, int position) {
    // Generate key using position
    int base_key = (position * key_multiplier + key_offset) % 256;
    
    // Add some complex but deterministic mathematical operations
    double floating_modifier = sin(position * 0.1) * 100;
    int int_modifier = (int)floating_modifier % 256;
    
    // XOR with multiple layers
    unsigned char step1 = encrypted_byte ^ base_key;
    unsigned char step2 = step1 ^ (int_modifier & 0xFF);
    unsigned char step3 = step2 ^ (int_modifier & 0xFF);  // XOR twice to cancel out
    
    // Apply bit rotation based on position
    int rotation = position % 8;
    unsigned char rotated = (step3 << rotation) | (step3 >> (8 - rotation));
    
    // Final XOR to get original character
    return rotated ^ ((rotation * 13) % 256) ^ ((rotation * 13) % 256);  // Cancel out again
}

// Wasteful computation function
void waste_time() {
    printf("Initializing quantum flux capacitor...\n");
    fflush(stdout);
    
    // Calculate some large fibonacci numbers (very slow)
    for (int i = 35; i <= 38; i++) {
        printf("Computing fibonacci(%d)...\n", i);
        fflush(stdout);
        long long result = slow_fibonacci(i);
        printf("F(%d) = %lld\n", i, result);
    }
    
    printf("Searching for large primes...\n");
    fflush(stdout);
    
    // Find some primes in a slow way
    long long start = 1000000;
    int found = 0;
    for (long long i = start; found < 3; i++) {
        if (is_prime_slow(i)) {
            printf("Found prime: %lld\n", i);
            found++;
        }
    }
    
    printf("Performing matrix calculations...\n");
    fflush(stdout);
    
    // Useless matrix multiplication
    const int size = 500;
    double **matrix_a = malloc(size * sizeof(double*));
    double **matrix_b = malloc(size * sizeof(double*));
    double **result = malloc(size * sizeof(double*));
    
    for (int i = 0; i < size; i++) {
        matrix_a[i] = malloc(size * sizeof(double));
        matrix_b[i] = malloc(size * sizeof(double));
        result[i] = malloc(size * sizeof(double));
        
        for (int j = 0; j < size; j++) {
            matrix_a[i][j] = i + j + 1.0;
            matrix_b[i][j] = i * j + 1.0;
            result[i][j] = 0.0;
        }
    }
    
    // Slow matrix multiplication
    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++) {
            for (int k = 0; k < size; k++) {
                result[i][j] += matrix_a[i][k] * matrix_b[k][j];
            }
        }
    }
    
    printf("Matrix calculation complete. Sum of first row: %.2f\n", 
           result[0][0] + result[0][1] + result[0][2]);
    
    // Cleanup
    for (int i = 0; i < size; i++) {
        free(matrix_a[i]);
        free(matrix_b[i]);
        free(result[i]);
    }
    free(matrix_a);
    free(matrix_b);
    free(result);
}

void decrypt_and_print_flag() {
    printf("\n" "="*50 "\n");
    printf("DECRYPTION SEQUENCE INITIATED\n");
    printf("="*50 "\n");
    
    char *flag = malloc(flag_length + 1);
    if (!flag) {
        printf("Memory allocation failed!\n");
        exit(1);
    }
    
    printf("Applying multi-layer cryptographic transformations...\n");
    
    for (int i = 0; i < flag_length; i++) {
        // Add artificial delay for each character
        usleep(100000);  // 0.1 second delay per character
        
        printf("Decrypting byte %d/%d...\r", i + 1, flag_length);
        fflush(stdout);
        
        flag[i] = complex_decrypt_byte(encrypted_flag[i], i);
    }
    
    flag[flag_length] = '\0';
    
    printf("\n\nDECRYPTION COMPLETE!\n");
    printf("FLAG: %s\n", flag);
    
    free(flag);
}

int main() {
    printf("CTF Challenge: Optimization Master\n");
    printf("===================================\n\n");
    printf("This program will eventually print the flag, but it's REALLY slow...\n");
    printf("Your goal: Optimize the binary to get the flag faster!\n\n");
    
    waste_time();
    decrypt_and_print_flag();
    
    return 0;
}
