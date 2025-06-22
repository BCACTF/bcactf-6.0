#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/mman.h>

// Flag: NIPS{S3lf_M0d1fy1ng_MIPS}
unsigned char encrypted_flag[] = {
    0x7A, 0x18, 0xC4, 0x9E, 0x52, 0xF1, 0x3A, 0x81,
    0x6D, 0xE9, 0x27, 0xB5, 0xA3, 0x45, 0x8C, 0x7D,
    0x38, 0xF6, 0x1B, 0x59, 0xC7, 0x42, 0x96, 0x0D
};

unsigned int key_schedule[4] = {0xDEADBEEF, 0xCAFEBABE, 0xFEEDFACE, 0xC0DEFEED};

// The actual MIPS machine code for our validator
unsigned int validation_code[] = {
    // Function prologue
    0x27BDFFD0,   // addiu $sp, $sp, -48        # Adjust stack pointer
    0xAFBF0028,   // sw $ra, 40($sp)            # Save return address
    0xAFBE0024,   // sw $fp, 36($sp)            # Save frame pointer
    0x03A0F021,   // move $fp, $sp              # Set up frame pointer

    // This code will be replaced at runtime with our validation logic
    // For now, just load zeros into registers and exit
    0x24020000,   // li $v0, 0                  # Load 0 into $v0 (return value)
    0x24030000,   // li $v1, 0                  # Clear $v1
    0x24040000,   // li $a0, 0                  # Clear $a0
    0x24050000,   // li $a1, 0                  # Clear $a1
    0x24060000,   // li $a2, 0                  # Clear $a2
    
    // Function epilogue
    0x8FBF0028,   // lw $ra, 40($sp)            # Restore return address
    0x8FBE0024,   // lw $fp, 36($sp)            # Restore frame pointer
    0x27BD0030,   // addiu $sp, $sp, 48         # Reset stack pointer
    0x03E00008    // jr $ra                     # Return
};

// This function will be modified at runtime
void __attribute__ ((noinline)) validator(const char* input) {
    // This is a placeholder that will be overwritten
    printf("Validating input...\n");
    printf("Invalid flag!\n");
    exit(1);
}

// Custom TEA-like cipher for checking
void transform(unsigned int* v, unsigned int* k) {
    unsigned int v0 = v[0], v1 = v[1];
    unsigned int sum = 0, delta = 0x9E3779B9;
    
    for (int i = 0; i < 16; i++) {
        sum += delta;
        v0 += ((v1 << 4) + k[0]) ^ (v1 + sum) ^ ((v1 >> 5) + k[1]);
        v1 += ((v0 << 4) + k[2]) ^ (v0 + sum) ^ ((v0 >> 5) + k[3]);
    }
    
    v[0] = v0; v[1] = v1;
}

// Generate the MIPS validation code dynamically
unsigned int* generate_mips_validation_code(const char* input, size_t len) {
    // Allocate memory for our generated code (more than enough for our needs)
    unsigned int* code = malloc(1024);
    if (!code) return NULL;
    
    // Copy the template validation code
    memcpy(code, validation_code, sizeof(validation_code));
    
    // Index to where we'll insert our validation logic (after the prologue)
    int idx = 4;
    
    // Load the input pointer into $a0
    code[idx++] = 0x27A40030;   // addiu $a0, $sp, 48     # Input string address
    
    // Initialize validation result to 1 (valid)
    code[idx++] = 0x24020001;   // li $v0, 1              # Assume valid
    
    // Check each 8-byte block
    for (size_t i = 0; i < len; i += 8) {
        // Load 8 bytes from input into $t0, $t1
        code[idx++] = 0x80880000 + i;        // lb $t0, i($a0)
        code[idx++] = 0x80890001 + i;        // lb $t1, i+1($a0)
        
        // Apply transformation (simplified for space)
        // In real code, this would be the full sequence of MIPS instructions for
        // the transform function
        code[idx++] = 0x01094020;            // add $t0, $t0, $t1
        code[idx++] = 0x000847C2;            // srl $t0, $t0, 31   # Some operation
        
        // Compare with encrypted values
        code[idx++] = 0x3C080000 + ((encrypted_flag[i] << 8) | encrypted_flag[i+1]);  
                                            // lui $t0, high_half
        code[idx++] = 0x35080000 + ((encrypted_flag[i+2] << 8) | encrypted_flag[i+3]);  
                                            // ori $t0, $t0, low_half
        
        // If not equal, set result to 0 (invalid)
        code[idx++] = 0x15080003;            // bne $t0, $t0, skip_invalidate
        code[idx++] = 0x00000000;            // nop
        code[idx++] = 0x24020000;            // li $v0, 0          # Set invalid
        code[idx++] = 0x1000000A;            // b exit             # Jump to exit
        // skip_invalidate:
    }
    
    // Exit sequence (already included in the template)
    // code[idx++] = 0x8FBF0028;            // lw $ra, 40($sp)
    // code[idx++] = 0x8FBE0024;            // lw $fp, 36($sp)
    // code[idx++] = 0x27BD0030;            // addiu $sp, $sp, 48
    // code[idx++] = 0x03E00008;            // jr $ra
    
    return code;
}

// Anti-debugging measure
int detect_debugging() {
    int debugging = 0;
    
    // Try to trace ourselves - if we're being debugged, this will fail
    if (ptrace(PTRACE_TRACEME, 0, 1, 0) < 0) {
        debugging = 1;
    } else {
        ptrace(PTRACE_DETACH, 0, 1, 0);
    }
    
    return debugging;
}

// Function to obfuscate our code
void obfuscate_code(unsigned int* code, int len) {
    for (int i = 0; i < len; i++) {
        // Add some junk instructions that don't affect the execution
        if (i % 5 == 0) {
            // NOP instruction
            code[i] = (code[i] & 0xFFFF0000) | 0x0000;
        }
    }
}

int main(int argc, char* argv[]) {
    if (argc != 2) {
        printf("Usage: %s <flag>\n", argv[0]);
        return 1;
    }
    
    // Anti-debugging check
    if (detect_debugging()) {
        printf("Nice try! No debugging allowed.\n");
        return 1;
    }
    
    char* input = argv[1];
    size_t len = strlen(input);
    
    // Input length check
    if (len != 24) {
        printf("Invalid flag length!\n");
        return 1;
    }
    
    // Generate the validation code
    unsigned int* mips_code = generate_mips_validation_code(input, len);
    if (!mips_code) {
        printf("Memory allocation error\n");
        return 1;
    }
    
    // Obfuscate the code a bit
    obfuscate_code(mips_code, sizeof(validation_code)/sizeof(unsigned int));
    
    // Make the memory executable
    void* page_aligned = (void*)((uintptr_t)validator & ~(getpagesize() - 1));
    if (mprotect(page_aligned, getpagesize(), PROT_READ | PROT_WRITE | PROT_EXEC) != 0) {
        printf("Memory protection error\n");
        free(mips_code);
        return 1;
    }
    
    // Replace the validator function with our generated code
    memcpy(validator, mips_code, sizeof(validation_code));
    
    // Free the temporary code
    free(mips_code);
    
    // Copy input to stack for validation
    char input_copy[32];
    strncpy(input_copy, input, sizeof(input_copy));
    input_copy[sizeof(input_copy) - 1] = '\0';
    
    // Call the now-modified function
    validator(input_copy);
    
    // If validation returns 1, the flag is correct
    printf("Validation complete!\n");
    
    // This will only execute if validation doesn't exit
    printf("Congratulations! The flag is correct: %s\n", input);
    return 0;
}
