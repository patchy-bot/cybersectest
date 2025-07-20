#include <stdio.h>
#include <string.h>

// Removed system("/bin/sh") call to prevent arbitrary code execution
// Instead, provide a safe interpreter loop without shell execution

int main() {
    char input[256];
    printf("Enter command (no shell access): ");
    if (fgets(input, sizeof(input), stdin) != NULL) {
        // Process input safely here
        printf("You entered: %s", input);
    }
    return 0;
}
