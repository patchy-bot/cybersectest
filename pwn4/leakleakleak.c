#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Example safe heap usage with checks
int main() {
    char *ptr = malloc(100);
    if (!ptr) {
        fprintf(stderr, "Memory allocation failed\n");
        return 1;
    }
    strcpy(ptr, "Safe heap usage example");
    printf("%s\n", ptr);
    // Properly free memory and nullify pointer to avoid use-after-free
    free(ptr);
    ptr = NULL;
    // Access after free is prevented by null check
    if (ptr != NULL) {
        printf("%s\n", ptr);
    } else {
        printf("Pointer is NULL, safe from use-after-free\n");
    }
    return 0;
}
