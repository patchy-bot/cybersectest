#include <stdio.h>
#include <string.h>

int main() {
    char buffer[64];
    printf("Enter data: ");
    if (fgets(buffer, sizeof(buffer), stdin) == NULL) return 1;
    // ensure NUL-terminated
    buffer[strcspn(buffer, "\n")] = '\0';
    printf("You entered: %s\n", buffer);
    return 0;
}