#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int evaluate_expression(const char *expr) {
    // Very simple evaluator that only allows digits and '+'
    int sum = 0;
    for (const char *p = expr; *p; ++p) {
        if (*p == '+') continue;
        if (*p < '0' || *p > '9') {
            printf("Invalid character in expression\n");
            return -1;
        }
        sum += *p - '0';
    }
    return sum;
}

int main() {
    char expr[128];
    printf("Enter sum expression (e.g. 1+2+3): ");
    if (!fgets(expr, sizeof(expr), stdin)) {
        perror("fgets");
        return 1;
    }
    expr[strcspn(expr, "\n")] = '\0';
    int result = evaluate_expression(expr);
    if (result >= 0) {
        printf("Result: %d\n", result);
    }
    return 0;
}