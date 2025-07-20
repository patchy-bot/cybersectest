#include <stdio.h>
#include <string.h>

int main(void) {
    char name[100];
    printf("Enter your name: ");
    if (fgets(name, sizeof(name), stdin) == NULL) {
        fprintf(stderr, "Error reading input\n");
        return 1;
    }
    /* Strip trailing newline, if any */
    name[strcspn(name, "\n")] = '\0';
    /* Use explicit format string to avoid format-string attacks */
    printf("Hello, %s!\n", name);
    return 0;
}