#include <stdio.h>
#include <stdlib.h>

int main() {
    char buf[128];
    printf("Enter your message: ");
    if (!fgets(buf, sizeof(buf), stdin)) {
        perror("fgets");
        return 1;
    }
    // Do not leak addresses to user
    printf("Message: %s", buf);
    return 0;
}