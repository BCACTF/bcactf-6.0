#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <stdbool.h>

// Global variables
char mango_flavor[64];
void *water_ptr = NULL;
void *mango_ptr = NULL;
char *secret_ingredient = NULL;

void setup() {
    setvbuf(stdout, NULL, _IONBF, 0);
    setvbuf(stderr, NULL, _IONBF, 0);
    setvbuf(stdin, NULL, _IONBF, 0);
}

void win() {
    if (secret_ingredient != NULL && strcmp(secret_ingredient, "respected") == 0) {
        printf("🌊 Still water + mango = Respected 🥭\n");
        system("/bin/sh");
    } else {
        printf("You haven't unlocked the secret ingredient yet!\n");
    }
}

// Vulnerability 1: Format string vulnerability
void view_recipe() {
    char input[128];
    printf("What recipe details would you like to see?\n> ");
    fgets(input, sizeof(input), stdin);
    input[strcspn(input, "\n")] = 0;
    
    // Format string vulnerability
    printf("Recipe details: ");
    printf(input);
    printf("\n");
}

// Vulnerability 2: Buffer overflow
void add_water() {
    char buffer[24];
    
    printf("Add some still water (describe how much):\n> ");
    // Buffer overflow vulnerability
    gets(buffer);
    
    water_ptr = malloc(64);
    strcpy(water_ptr, "still water");
    printf("Added %s to your drink!\n", (char*)water_ptr);
}

// Vulnerability 3: Use-after-free
void add_mango() {
    if (!water_ptr) {
        printf("You need to add water first!\n");
        return;
    }
    
    printf("Adding mango...\n");
    mango_ptr = malloc(64);
    strcpy(mango_ptr, "mango slice");
    
    printf("Enter mango flavor: ");
    fgets(mango_flavor, sizeof(mango_flavor), stdin);
    
    printf("Do you want to remove the mango? (y/n)\n> ");
    char choice;
    scanf(" %c", &choice);
    getchar(); // Consume newline
    
    if (choice == 'y') {
        free(mango_ptr);  // Use-after-free: pointer not nulled
        printf("Mango removed. You can add it again later.\n");
    }
}

// Vulnerability 4: Integer overflow
void add_secret_ingredient() {
    if (!water_ptr) {
        printf("You need to add water first!\n");
        return;
    }
    
    unsigned short length;
    char ingredient_buffer[32];
    
    printf("Enter secret ingredient length: ");
    scanf("%hu", &length);
    getchar(); // Consume newline
    
    // Integer overflow vulnerability
    if (length > sizeof(ingredient_buffer)) {
        printf("Ingredient name too long!\n");
        return;
    }
    
    printf("Enter secret ingredient name: ");
    // If length is manipulated via integer overflow, can write beyond buffer
    read(0, ingredient_buffer, length);
    ingredient_buffer[31] = '\0'; // Null terminate, but doesn't help if overflow occurs
    
    secret_ingredient = strdup(ingredient_buffer);
    printf("Secret ingredient added: %s\n", secret_ingredient);
}

void mix_drink() {
    if (!water_ptr) {
        printf("You need to add water first!\n");
        return;
    }
    
    printf("Mixing drink with what you have...\n");
    
    if (mango_ptr) {
        printf("Your still water + mango drink is ready!\n");
        // If memory was properly manipulated, win() might be called
    } else {
        printf("Your drink is just water. Not impressive.\n");
    }
}

void show_menu() {
    printf("\n🌊🥭 Still Water + Mango Mixer 🥭🌊\n");
    printf("1. View recipe\n");
    printf("2. Add still water\n");
    printf("3. Add mango\n");
    printf("4. Add secret ingredient\n");
    printf("5. Mix drink\n");
    printf("6. Win respect\n");
    printf("7. Exit\n");
    printf("> ");
}

int main() {
    setup();
    int choice;
    
    printf("Welcome to the Still Water + Mango challenge!\n");
    printf("Can you make the perfect drink to win respect?\n");
    
    while (1) {
        show_menu();
        scanf("%d", &choice);
        getchar(); // Consume newline
        
        switch (choice) {
            case 1:
                view_recipe();
                break;
            case 2:
                add_water();
                break;
            case 3:
                add_mango();
                break;
            case 4:
                add_secret_ingredient();
                break;
            case 5:
                mix_drink();
                break;
            case 6:
                win();
                break;
            case 7:
                printf("Goodbye!\n");
                exit(0);
            default:
                printf("Invalid choice!\n");
        }
    }
    
    return 0;
}
