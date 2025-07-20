#include <stdio.h>
#include <stdlib.h>

int main() {
    char buf[128];
    printf("Enter some text: ");
    if (fgets(buf, sizeof(buf), stdin) == NULL) {
        perror("fgets");
        return 1;
    }
    buf[strcspn(buf, "\n")] = '\0';
    printf("Output: %s\n", buf);
    return 0;
}