#include <stdio.h>
#include <stdlib.h>

int main() {
    char input[256];
    printf("Enter your comment: ");
    if (!fgets(input, sizeof(input), stdin)) {
        perror("fgets");
        return 1;
    }
    // Remove trailing newline
    size_t len = strcspn(input, "\n");
    input[len] = '\0';
    // Print user input safely with format specifier
    printf("User says: %s\n", input);
    return 0;
}