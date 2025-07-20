#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int main() {
    char *p = malloc(64);
    if (!p) {
        perror("malloc"); return 1;
    }
    printf("Enter text: ");
    if (fgets(p, 64, stdin) == NULL) {
        free(p);
        return 1;
    }
    p[strcspn(p, "\n")] = '\0';
    printf("You typed: %s\n", p);
    // Securely zero and free
    memset(p, 0, 64);
    free(p);
    return 0;
}