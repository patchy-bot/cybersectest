#include <stdlib.h>
#include <stdio.h>

int main() {
    size_t size;
    char *data;
    printf("Enter size: ");
    if (scanf("%zu", &size) != 1 || size > 1024) {
        fprintf(stderr, "Invalid or too large size\n");
        return 1;
    }
    data = malloc(size);
    if (!data) { perror("malloc"); return 1; }
    // initialize and use data safely
    memset(data, 0, size);
    printf("Allocated %zu bytes\n", size);
    free(data);
    return 0;
}