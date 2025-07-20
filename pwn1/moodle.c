#include <stdio.h>
#include <string.h>

int main() {
    char name[100];
    printf("Enter your name: ");
    fgets(name, sizeof(name), stdin);
    // Remove newline character if present
    name[strcspn(name, "\n")] = 0;
    // Use a fixed format string to prevent format string vulnerability
    printf("Hello, %s!\n", name);
    return 0;
}
