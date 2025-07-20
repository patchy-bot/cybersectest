#include <stdio.h>
#include <string.h>

int main() {
    char buffer[100];
    printf("Enter input: ");
    // Use fgets instead of gets to prevent buffer overflow
    if (fgets(buffer, sizeof(buffer), stdin) != NULL) {
        // Remove newline character if present
        buffer[strcspn(buffer, "\n")] = 0;
        printf("You entered: %s\n", buffer);
    } else {
        printf("Input error.\n");
    }
    return 0;
}
