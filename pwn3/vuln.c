#include <stdio.h>
#include <string.h>

#define INPUT_SIZE 128

int main(void) {
    char data[INPUT_SIZE];
    printf("Input data: ");
    // Safe read
    if (fgets(data, sizeof(data), stdin) == NULL) {
        perror("fgets failed");
        return 1;
    }
    // Remove newline
    data[strcspn(data, "\n")] = '\0';
    // Safe processing
    printf("Processed: %s\n", data);
    return 0;
}