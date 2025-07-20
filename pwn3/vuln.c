#include <stdio.h>
#include <string.h>

int main() {
    char buf[128];
    printf("Enter data: ");
    if (fgets(buf, sizeof(buf), stdin) == NULL) {
        return 1;
    }
    // Strip newline
    buf[strcspn(buf, "\n")] = '\0';
    printf("Data: %s\n", buf);
    return 0;
}