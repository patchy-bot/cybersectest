#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Removed system("/bin/sh") call and replaced with safe command execution example
int main() {
    char input[100];
    printf("Enter command (only 'help' or 'exit' allowed): ");
    if (fgets(input, sizeof(input), stdin) != NULL) {
        input[strcspn(input, "\n")] = 0;
        // Whitelist allowed commands
        if (strcmp(input, "help") == 0) {
            printf("Available commands: help, exit\n");
        } else if (strcmp(input, "exit") == 0) {
            printf("Exiting...\n");
            return 0;
        } else {
            printf("Invalid command.\n");
        }
    }
    return 0;
}
