#include <stdio.h>
#include <stdlib.h>

int main() {
    char buffer[64];
    printf("Enter input: ");
    if (fgets(buffer, sizeof(buffer), stdin) == NULL) {
        fprintf(stderr, "Input error\n");
        return 1;
    }
    buffer[strcspn(buffer, "\n")] = '\0';
    printf("You entered: %s\n", buffer);
    return 0;
}