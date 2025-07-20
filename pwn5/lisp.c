#include <stdio.h>
#include <string.h>
#include <stdlib.h>

void eval(const char *expr) {
    // Forbid system calls; implement a safe interpreter
    if (strstr(expr, "system(") || strstr(expr, "exec")) {
        fprintf(stderr, "Disallowed function in expression\n");
        return;
    }
    // A placeholder safe evaluation: only digits and + - * /
    for (size_t i = 0; i < strlen(expr); ++i) {
        if (!(isdigit(expr[i]) || strchr("+-*/ ()", expr[i]))) {
            fprintf(stderr, "Invalid character\n");
            return;
        }
    }
    // Implement a real parser here
    printf("Result: [safe eval not implemented]\n");
}

int main() {
    char expr[256];
    printf("Enter expression: ");
    if (!fgets(expr, sizeof(expr), stdin)) return 1;
    expr[strcspn(expr, "\n")] = '\0';
    eval(expr);
    return 0;
}