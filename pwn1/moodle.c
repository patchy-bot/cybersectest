#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(int argc, char *argv[]) {
    char input[256];
    if (argc != 2) {
        fprintf(stderr, "Usage: %s <string>\n", argv[0]);
        return EXIT_FAILURE;
    }
    /* Copy at most sizeof(input)-1 chars, ensure NUL-termination */
    strncpy(input, argv[1], sizeof(input) - 1);
    input[sizeof(input) - 1] = '\0';
    /* Use a fixed format specifier to avoid format-string vulnerability */
    printf("User input: %s\n", input);
    return EXIT_SUCCESS;
}