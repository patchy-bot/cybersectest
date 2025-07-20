#include <stdio.h>
#include <stdlib.h>
#include <string.h>

char* allocate(void) {
    char *p = malloc(64);
    if (!p) {
        fprintf(stderr, "Allocation failed\n");
        exit(1);
    }
    strcpy(p, "Hello, secure world!");
    return p;
}

int main(void) {
    char *data = allocate();
    /* Use the allocated memory before freeing */
    printf("Allocated data: %s\n", data);
    free(data);
    data = NULL;  /* Avoid use-after-free */
    return 0;
}