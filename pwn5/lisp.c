#include <stdio.h>
#include <string.h>
#include <unistd.h>

int main() {
    char input[128];
    printf("Enter Lisp expression: ");
    if (fgets(input, sizeof(input), stdin) == NULL) return 1;
    input[strcspn(input, "\n")] = '\0';
    // Do not call system on untrusted input
    printf("You typed: %s\n", input);
    // TODO: Implement a safe interpreter without spawning shell
    return 0;
}