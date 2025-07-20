#include <stdio.h>
#include <stdlib.h>

int main() {
    char buf[64];
    printf("Enter data: ");
    // Use fgets to limit input to buffer size - 1, reserve for '\0'
    if (!fgets(buf, sizeof(buf), stdin)) {
        perror("fgets");
        return 1;
    }
    // Process input safely
    printf("You entered: %s", buf);
    return 0;
}