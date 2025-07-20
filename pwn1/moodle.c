#include <stdio.h>
#include <string.h>

#define MAX_NAME_LEN 100

void greet(const char *name) {
    char safe_name[MAX_NAME_LEN + 1];
    // Copy with bounds checking to avoid overflow
    strncpy(safe_name, name, MAX_NAME_LEN);
    safe_name[MAX_NAME_LEN] = '\0';
    // Use a format string with specifier to prevent format‐string vulnerabilities
    printf("Hello, %s!\n", safe_name);
}

int main(void) {
    char name[MAX_NAME_LEN + 1];
    // Read input safely
    if (fgets(name, sizeof(name), stdin) != NULL) {
        // Strip newline
        name[strcspn(name, "\n")] = '\0';
        greet(name);
    }
    return 0;
}