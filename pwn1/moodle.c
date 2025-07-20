#include <stdio.h>
#include <string.h>

void print_name(const char *name) {
    // Use a fixed format string to prevent format string vulnerability
    printf("User name: %s\n", name);
}

int main() {
    char name[100];
    printf("Enter your name: ");
    fgets(name, sizeof(name), stdin);
    // Remove newline character if present
    name[strcspn(name, "\n")] = 0;
    print_name(name);
    return 0;
}
