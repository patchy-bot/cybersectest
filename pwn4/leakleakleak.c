#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct Node {
    char data[64];
    struct Node *next;
} Node;

int main() {
    Node *head = malloc(sizeof(Node));
    if (!head) return 1;
    // Initialize safely
    strncpy(head->data, "Hello, world!", sizeof(head->data)-1);
    head->data[sizeof(head->data)-1] = '\0';
    head->next = NULL;

    printf("Stored data: %s\n", head->data);

    // Free and nullify to prevent use-after-free
    free(head);
    head = NULL;

    // Any further use of head should be checked
    if (head) {
        printf("Node still present\n");
    } else {
        printf("Node has been freed\n");
    }
    return 0;
}