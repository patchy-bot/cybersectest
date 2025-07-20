#include <stdio.h>
#include <string.h>

int main(void) {
    char buf[64];
    printf("Enter text: ");
    /* Use fgets to prevent buffer overflow; reserve space for null terminator */
    if (fgets(buf, sizeof(buf), stdin) == NULL) {
        fprintf(stderr, "Input error\n");
        return 1;
    }
    /* Strip trailing newline if present */
    buf[strcspn(buf, "\n")] = '\0';
    printf("You entered: %s\n", buf);
    return 0;
}