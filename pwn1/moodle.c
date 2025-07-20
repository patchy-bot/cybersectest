#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main() {
    char name[100];
    printf("Enter your name: ");
    if (fgets(name, sizeof(name), stdin) == NULL) {
        fprintf(stderr, "Input error\n");
        return 1;
    }
    /* Remove possible newline */
    name[strcspn(name, "\n")] = '\0';
    /* Use format specifier to prevent format string vulnerability */
    printf("Hello, %s\n", name);
    return 0;
}