#include "stdio.h"
#include "string.h"

unsigned short data[40] = {65416, 65415, 65426, 65436, 65419, 65433, 65412, 65464, 65487, 65435, 65440, 65467, 65483, 65426, 65426, 65486, 65419, 65440, 65451, 65486, 65426, 65426, 65414, 65410};

int check(char input[]) {
    if (strlen(input) < 24) {
        return 1;
    }
    for (int i = 0; i < strlen(input);  i++) {
        if ((unsigned short)(~input[i]) != data[i]) {
            return 1;
        }
    }
    return 0;
}

int main() {
    char input[40];

    printf("Enter your flag:");
    scanf("%s", input);
    if (check(input) == 0) {
        printf("Good Job!\n");
    } else {
        printf("Incorrect. Try again.\n");
    }
}
