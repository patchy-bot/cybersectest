#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_CHUNK 256

void safe_read(char *buf, size_t size) {
    if (fgets(buf, size, stdin) == NULL) {
        fprintf(stderr, "Input error\n");
        exit(1);
    }
    buf[strcspn(buf, "\n")] = '\0';
}

int main() {
    char *p = malloc(MAX_CHUNK);
    if (!p) {
        perror("malloc");
        return 1;
    }
    printf("Enter data: ");
    safe_read(p, MAX_CHUNK);
    printf("You said: %s\n", p);
    free(p);
    return 0;
}