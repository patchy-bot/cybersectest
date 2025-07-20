#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* A minimal, safe LISP-like evaluator without system() */
int eval(const char *expr) {
    /* Dummy implementation: only supports integers and + */
    int a, b;
    if (sscanf(expr, "%d + %d", &a, &b) == 2) {
        return a + b;
    }
    return 0;
}

int main(void) {
    char buf[256];
    printf("Enter expression (e.g. 1 + 2): ");
    if (!fgets(buf, sizeof(buf), stdin)) return 1;
    size_t len = strlen(buf);
    if (len && buf[len-1]=='\n') buf[len-1]='\0';
    int result = eval(buf);
    printf("Result: %d\n", result);
    return 0;
}