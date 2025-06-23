#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/wait.h>
#include <signal.h>
#include <time.h>
#include <fcntl.h>
#include <stdint.h>
#include "flag_constants.h"

#ifdef __linux__
#include <sys/ptrace.h>
#else
// Fallback definitions for macOS
#define PTRACE_TRACEME 0
#define PTRACE_DETACH 11
extern int ptrace(int request, int pid, void *addr, int data);
#endif

// Global validation state
static int validation_initialized = 0;

// TEA key schedule (same as in generate_flag.py)
unsigned int key_schedule[4] = {0xDEADBEEF, 0xCAFEBABE, 0xFEEDFACE, 0xC0DEFEED};

// Template for MIPS machine code that will be used for validation
unsigned char validation_template[] = {
    // Simple function that returns 1 if input matches decrypted flag
    0x24, 0x02, 0x00, 0x01,        // li $v0, 1
    0x03, 0xe0, 0x00, 0x08,        // jr $ra
    0x00, 0x00, 0x00, 0x00         // nop (delay slot)
};

// Forward declaration
int main(int argc, char* argv[]);

// This function will be modified at runtime
void __attribute__ ((noinline)) validator(const char* input) {
    // This is a placeholder that will be overwritten
    printf("Validating input...\n");
    printf("Invalid flag!\n");
    exit(1);
}

// TEA encryption function
void tea_encrypt(unsigned int* v, unsigned int* k) {
    unsigned int v0 = v[0], v1 = v[1];
    unsigned int sum = 0, delta = 0x9E3779B9;
    
    for (int i = 0; i < 32; i++) {
        sum += delta;
        v0 += ((v1 << 4) + k[0]) ^ (v1 + sum) ^ ((v1 >> 5) + k[1]);
        v1 += ((v0 << 4) + k[2]) ^ (v0 + sum) ^ ((v0 >> 5) + k[3]);
    }
    
    v[0] = v0; v[1] = v1;
}

// TEA decryption function
void tea_decrypt(unsigned int* v, unsigned int* k) {
    unsigned int v0 = v[0], v1 = v[1];
    unsigned int sum = 0xC6EF3720, delta = 0x9E3779B9;  // sum = delta * 32
    
    for (int i = 0; i < 32; i++) {
        v1 -= ((v0 << 4) + k[2]) ^ (v0 + sum) ^ ((v0 >> 5) + k[3]);
        v0 -= ((v1 << 4) + k[0]) ^ (v1 + sum) ^ ((v1 >> 5) + k[1]);
        sum -= delta;
    }
    
    v[0] = v0; v[1] = v1;
}

// Initialize the validation system
void init_validation_system() {
    if (validation_initialized) return;
    validation_initialized = 1;
}

// Generate MIPS validation code dynamically
unsigned char* generate_validation_code(const char* input, size_t len) {
    // Allocate memory for our generated code
    unsigned char* code = malloc(1024);
    if (!code) return NULL;
    
    // For simplicity, just validate by comparing TEA-encrypted input with stored encrypted flag
    // The actual validation will be done in the main function before calling this
    
    // Copy simple return-success template
    memcpy(code, validation_template, sizeof(validation_template));
    
    return code;
}

// Multiple anti-debugging measures
volatile int debug_detected = 0;

// Check for debugger via ptrace
int check_ptrace() {
#ifdef __linux__
    if (ptrace(PTRACE_TRACEME, 0, 1, 0) < 0) {
        return 1;
    }
    ptrace(PTRACE_DETACH, 0, 1, 0);
#else
    // macOS ptrace has different signature
    if (ptrace(PTRACE_TRACEME, 0, (void*)1, 0) < 0) {
        return 1;
    }
    ptrace(PTRACE_DETACH, 0, (void*)1, 0);
#endif
    return 0;
}

// Check for debugger via /proc/self/status
int check_proc_status() {
    FILE *f = fopen("/proc/self/status", "r");
    if (!f) return 0;
    
    char line[256];
    while (fgets(line, sizeof(line), f)) {
        if (strncmp(line, "TracerPid:", 10) == 0) {
            int tracer_pid = atoi(line + 10);
            fclose(f);
            return tracer_pid != 0;
        }
    }
    fclose(f);
    return 0;
}

// Timing-based anti-debugging
int check_timing() {
    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);
    
    // Simple operation that should be fast
    volatile int x = 0;
    for (int i = 0; i < 1000; i++) {
        x += i;
    }
    
    clock_gettime(CLOCK_MONOTONIC, &end);
    long diff = (end.tv_sec - start.tv_sec) * 1000000000L + (end.tv_nsec - start.tv_nsec);
    
    // If it takes more than 1ms, probably being debugged
    return diff > 1000000;
}

// Check for common debugger environment variables
int check_env_vars() {
    char* debug_vars[] = {"GDB", "STRACE", "LTRACE", "LD_PRELOAD", NULL};
    for (int i = 0; debug_vars[i]; i++) {
        if (getenv(debug_vars[i])) {
            return 1;
        }
    }
    return 0;
}

// Anti-debugging signal handler
void sighandler(int sig) {
    debug_detected = 1;
    signal(sig, sighandler);
}

// Stack canary for tampering detection
static volatile unsigned int stack_canary = 0xDEADC0DE;
// Runtime integrity checking
unsigned int calculate_checksum(unsigned char* data, size_t len) {
    unsigned int checksum = 0x12345678;
    for (size_t i = 0; i < len; i++) {
        checksum = ((checksum << 1) | (checksum >> 31)) ^ data[i];
    }
    return checksum;
}

// Simple but effective debugging detection
int detect_debugging() {
    // Check stack canary integrity
    if (stack_canary != 0xDEADC0DE) {
        debug_detected = 1;
        return 1;
    }
    
    // Simple timing check - less sensitive than before
    struct timespec start, end;
    clock_gettime(CLOCK_MONOTONIC, &start);
    
    // Do some work
    volatile int sum = 0;
    for (int i = 0; i < 10000; i++) {
        sum += (i * 13 + 7) % 97;
    }
    
    clock_gettime(CLOCK_MONOTONIC, &end);
    long diff = (end.tv_sec - start.tv_sec) * 1000000000L + (end.tv_nsec - start.tv_nsec);
    
    // If it takes more than 10ms, might be debugged (more lenient)
    if (diff > 10000000) {
        debug_detected = 1;
    }
    
    // Check for obvious debug environment variables
    if (check_env_vars()) {
        debug_detected = 1;
    }
    
    // Anti-tampering: verify our own checksum
    static int first_run = 1;
    static unsigned int original_checksum = 0;
    
    if (first_run) {
        // Calculate checksum of main function area (first 1000 bytes)
        original_checksum = calculate_checksum((unsigned char*)main, 1000);
        first_run = 0;
    } else {
        // Verify checksum hasn't changed
        unsigned int current_checksum = calculate_checksum((unsigned char*)main, 1000);
        if (current_checksum != original_checksum) {
            debug_detected = 1;
        }
    }
    
    return debug_detected;
}

// Advanced code obfuscation techniques
void obfuscate_code(unsigned char* code, int len) {
    // XOR obfuscation with a dynamic key
    unsigned char xor_key = (unsigned char)((time(NULL) & 0xFF) ^ 0xAA);
    
    for (int i = 0; i < len; i++) {
        // Skip the function prologue and epilogue
        if (i < 10 || i > len - 10) continue;
        
        // Apply XOR obfuscation
        code[i] ^= xor_key;
        
        // Add some junk bytes at strategic locations
        if (i % 7 == 0 && i + 1 < len) {
            // Insert a NOP byte
            memmove(code + i + 1, code + i, len - i - 1);
            code[i] = 0x90; // NOP instruction
        }
    }
}

// Polymorphic code transformation
void morph_code(unsigned char* code, int len) {
    static int morph_counter = 0;
    morph_counter++;
    
    // Apply different transformations based on morph counter
    switch (morph_counter % 3) {
        case 0:
            // Bit rotation
            for (int i = 10; i < len - 10; i++) {
                code[i] = ((code[i] << 1) | (code[i] >> 7)) & 0xFF;
            }
            break;
        case 1:
            // Byte swapping
            for (int i = 10; i < len - 11; i += 2) {
                unsigned char temp = code[i];
                code[i] = code[i + 1];
                code[i + 1] = temp;
            }
            break;
        case 2:
            // Additive cipher
            for (int i = 10; i < len - 10; i++) {
                code[i] = (code[i] + (i & 0xFF)) & 0xFF;
            }
            break;
    }
}

// Function to add control flow obfuscation
void add_control_flow_obfuscation() {
    // Create fake execution paths
    volatile int fake_condition = 0;
    
    if (fake_condition) {
        // This will never execute but confuses static analysis
        printf("how TF did you end up here\n");
        exit(1);
    }
    
    // Add some useless computations
    volatile int x = 42;
    for (int i = 0; i < 10; i++) {
        x = (x * 13 + 7) % 97;
    }
}






int main(int argc, char* argv[]) {
    // Initialize validation system
    init_validation_system();
    
    // Add control flow obfuscation
    add_control_flow_obfuscation();
    
    if (argc != 2) {
        printf("Usage: %s <flag>\n", argv[0]);
        return 1;
    }
    printf("wow you got here! impressive 1\n");

    if (detect_debugging()) {
        printf("Nice try! No debugging allowed.\n");
        return 1;
    }

    printf("wow you got here! impressive 2\n");

    char* input = argv[1];
    size_t len = strlen(input);
    
    // Input length check
    if (len != ORIGINAL_FLAG_SIZE) {
        printf("Invalid flag length!\n");
        return 1;
    }

    printf("wow you got here! impressive 3\n");
    
    // TEA-encrypt the input and compare with stored encrypted flag
    unsigned char input_encrypted[ENCRYPTED_FLAG_SIZE];
    memset(input_encrypted, 0, sizeof(input_encrypted));

    printf("wow you got here! impressive 4\n");

    // Prepare input for encryption (pad to multiple of 8 bytes)
    unsigned char padded_input[32];
    memset(padded_input, 0, sizeof(padded_input));
    strncpy((char*)padded_input, input, len);
    
    printf("wow you got here! impressive 5\n");

    // Encrypt input using TEA
    for (int i = 0; i < ENCRYPTED_FLAG_SIZE; i += 8) {
        unsigned int block[2];
        memcpy(block, padded_input + i, 8);
        tea_encrypt(block, key_schedule);
        memcpy(input_encrypted + i, block, 8);
    }

    printf("wow you got here! impressive 6\n");
    
    // Compare encrypted input with stored encrypted flag
    if (memcmp(input_encrypted, encrypted_flag, ENCRYPTED_FLAG_SIZE) != 0) {
        printf("Invalid flag!\n");
        return 1;
    }

    printf("wow you got here! impressive 7\n");
    
    // Generate the validation code (for trolls)
    unsigned char* generated_code = generate_validation_code(input, len);
    if (!generated_code) {
        printf("Memory allocation error\n");
        return 1;
    }

    printf("wow you got here! impressive 7\n");
    
    // Apply obfuscation to the generated code
    obfuscate_code(generated_code, sizeof(validation_template));
    morph_code(generated_code, sizeof(validation_template));
    
    printf("wow you got here! impressive 8\n");

    // Allocate executable memory instead of modifying existing function
    size_t code_size = sizeof(validation_template);
    void* executable_mem = mmap(NULL, code_size, PROT_READ | PROT_WRITE | PROT_EXEC, 
                               MAP_PRIVATE | MAP_ANONYMOUS, -1, 0);
    
    if (executable_mem == MAP_FAILED) {
        printf("Memory allocation error for executable code\n");
        free(generated_code);
        return 1;
    }
    
    printf("wow you got here! impressive 9\n");

    // Copy the generated code to executable memory
    memcpy(executable_mem, generated_code, code_size);
    
    printf("wow you got here! impressive 9.5\n");
    
    // Update validator to point to our executable memory
    void (*dynamic_validator)(const char*) = (void (*)(const char*))executable_mem;
    
    printf("wow you got here! impressive 10\n");

    // Free the temporary code
    free(generated_code);
    
    printf("wow you got here! impressive 11\n");

    // Another anti-debugging check before calling the modified function
    if (detect_debugging()) {
        printf("Debugging detected during execution!\n");
        return 1;
    }

    printf("wow you got here! impressive 12\n");
    
    // Call the dynamically generated function
    // dynamic_validator(input); 
    // man screw ts i aint doing allat
    
    // Clean up executable memory
    munmap(executable_mem, code_size);
    
    printf("wow you got here! impressive 13\n");

    printf("Congratulations! The flag is correct: %s\n", input);

    printf("wow you got here! impressive 14\n");
    
    return 0;
}
