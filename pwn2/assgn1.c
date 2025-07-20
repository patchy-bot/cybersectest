#include <stdio.h>
#include <string.h>

int main() {
    char buf[64];
    printf("Enter input: ");
    if (fgets(buf, sizeof(buf), stdin) == NULL) {
        return 1;
    }
    // Remove trailing newline
    size_t len = strcspn(buf, "\n");
    buf[len] = '\0';
    printf("You entered: %s\n", buf);
    return 0;
}