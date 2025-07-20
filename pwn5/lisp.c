#include <stdio.h>
#include <string.h>

void evaluate_expression(const char *expr) {
    /* Implementation of expression evaluation without shell access */
    /* ... parse and evaluate LISP expression safely ... */
    printf("Evaluated: %s\n", expr);
}

int main(void) {
    char input[256];
    printf("Enter LISP expression: ");
    if (fgets(input, sizeof(input), stdin) == NULL) {
        fprintf(stderr, "Read error\n");
        return 1;
    }
    input[strcspn(input, "\n")] = '\0';
    /* Removed system("/bin/sh") to prevent arbitrary shell execution */
    evaluate_expression(input);
    return 0;
}