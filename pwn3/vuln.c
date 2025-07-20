#include <stdio.h>
#include <string.h>

int main() {
    char buf[128];
    printf("Input: ");
    if (fgets(buf, sizeof(buf), stdin) == NULL) return 1;
    buf[strcspn(buf, "\n")] = '\0';
    printf("Got: %s\n", buf);
    return 0;
}