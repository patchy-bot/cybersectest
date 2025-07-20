#include <stdio.h>
#include <string.h>

int main(int argc, char *argv[]) {
    char name[128];
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <name>\n", argv[0]);
        return 1;
    }
    // Copy and sanitize input: limit length and remove format specifiers
    strncpy(name, argv[1], sizeof(name) - 1);
    name[sizeof(name) - 1] = '\0';
    for (size_t i = 0; i < strlen(name); ++i) {
        if (name[i] == '%') {
            name[i] = '?';
        }
    }
    // Use constant format string to avoid format-string vulnerability
    printf("Hello, %s!\n", name);
    return 0;
}