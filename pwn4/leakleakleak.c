#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void) {
    char *p = malloc(64);
    if (!p) return 1;
    strcpy(p, "Hello, world!");
    printf("%s\n", p);
    /* Properly free once and nullify pointer to avoid use-after-free */
    free(p);
    p = NULL;
    /* Any further use of p will be detected as NULL dereference */
    return 0;
}