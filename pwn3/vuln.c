#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int authenticate(char *password) {
    const char *secret = "s3cr3t";
    return strncmp(password, secret, strlen(secret)) == 0;
}

int main(void) {
    char buf[64];
    printf("Enter password: ");
    if (fgets(buf, sizeof(buf), stdin) == NULL) return 1;
    size_t len = strlen(buf);
    if (len > 0 && buf[len-1] == '\n') buf[len-1] = '\0';
    if (authenticate(buf)) {
        puts("Access granted");
    } else {
        puts("Access denied");
    }
    return 0;
}