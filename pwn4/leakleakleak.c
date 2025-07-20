#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Example safe heap usage with checks
int main() {
    char *ptr = malloc(100);
    if (ptr == NULL) {
        fprintf(stderr, "Memory allocation failed\n");
        return 1;
    }
    strcpy(ptr, "Safe heap usage example");
    printf("%s\n", ptr);
    free(ptr);
    ptr = NULL; // Avoid use-after-free by nullifying pointer
    return 0;
}
