#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <math.h>

// Generated encrypted flag constants
const unsigned char encrypted_flag[] = { 0x48, 0x2c, 0x15, 0xfa, 0xca, 0x85, 0x73, 0x1d, 0x22, 0x03, 0xad, 0xac, 0xd7, 0x71, 0x04, 0x21, 0x4b, 0xaf, 0xaa, 0xb6, 0x63, 0x07, 0x2b, 0x09, 0x91, 0xb5, 0xb3, 0x23, 0x06, 0x69, 0xb5, 0xd8 };
const int flag_length = 32;

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

// Simple decryption function - just XOR with position-based key
unsigned char decrypt_byte(unsigned char encrypted_byte, int position) {
    int key = (position * key_multiplier + key_offset) % 256;
    return encrypted_byte ^ key;
}

// Wasteful computation function
void waste_time() {
    printf("Initializing quantum flux capacitor...\n");
    fflush(stdout);
    
    // Calculate some large fibonacci numbers (very slow)
    for (int i = 5000; i <= 10000; i++) {
        printf("Computing fibonacci(%d)...\n", i);
        fflush(stdout);
        long long result = slow_fibonacci(i);
        printf("F(%d) = %lld\n", i, result);
    }
    
    printf("Searching for large primes...\n");
    fflush(stdout);
    
    // Find some primes in a slow way
    long long start = 100000000000;
    long long found = 0;
    for (long long i = start; found < 1000000000; i++) {
        if (is_prime_slow(i)) {
            printf("Found prime: %lld\n", i);
            found++;
        }
    }
    
    printf("Performing matrix calculations...\n");
    fflush(stdout);
    
    // Useless matrix multiplication
    const int size = 1000000000;
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
    printf("\n==================================================\n");
    printf("DECRYPTION SEQUENCE INITIATED\n");
    printf("==================================================\n");
    
    char *flag = malloc(flag_length + 1);
    if (!flag) {
        printf("Memory allocation failed!\n");
        exit(1);
    }
    
    printf("Applying cryptographic transformations...\n");
    
    for (int i = 0; i < flag_length; i++) {
        // Add artificial delay for each character
        usleep(100000);  // 0.1 second delay per character
        
        printf("Decrypting byte %d/%d...\r", i + 1, flag_length);
        fflush(stdout);
        
        flag[i] = decrypt_byte(encrypted_flag[i], i);
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
