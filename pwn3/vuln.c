#include <stdio.h>
#include <string.h>

int main(void) {
    char buffer[128];
    printf("Enter your data: ");
    /* Safe read with fgets */
    if (fgets(buffer, sizeof(buffer), stdin) == NULL) {
        fprintf(stderr, "Error reading input\n");
        return 1;
    }
    buffer[strcspn(buffer, "\n")] = '\0';
    printf("Data: %s\n", buffer);
    return 0;
}