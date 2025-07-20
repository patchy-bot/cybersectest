#include <stdio.h>
#include <string.h>

#define BUF_SIZE 64

int main(void) {
    char buffer[BUF_SIZE];
    // Use fgets instead of gets to prevent overflow
    printf("Enter input: ");
    if (fgets(buffer, sizeof(buffer), stdin) == NULL) {
        perror("fgets failed");
        return 1;
    }
    // Remove trailing newline
    buffer[strcspn(buffer, "\n")] = '\0';
    printf("You entered: %s\n", buffer);
    return 0;
}