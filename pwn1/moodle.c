#include <stdio.h>
#include <string.h>

int main() {
    char name[128];
    printf("Enter your name: ");
    if (fgets(name, sizeof(name), stdin) == NULL) return 1;
    name[strcspn(name, "\n")] = '\0'; // strip newline
    // Use a format string literal to avoid format-string vuln
    printf("Hello, %s!\n", name);
    return 0;
}