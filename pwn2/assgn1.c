#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void) {
    char buf[128];
    /* Use fgets instead of gets, limit to sizeof(buf)-1 */
    printf("Enter input: ");
    if (fgets(buf, sizeof(buf), stdin) == NULL) {
        fprintf(stderr, "Input error\n");
        return EXIT_FAILURE;
    }
    /* Remove trailing newline if present */
    size_t len = strlen(buf);
    if (len > 0 && buf[len-1] == '\n') buf[len-1] = '\0';
    printf("You entered: %s\n", buf);
    return EXIT_SUCCESS;
}