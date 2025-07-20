#include <stdlib.h>
#include <stdio.h>
#include <string.h>

typedef struct Node {
    char *data;
    struct Node *next;
} Node;

Node* create_node(const char *text) {
    Node *n = malloc(sizeof(Node));
    if (!n) return NULL;
    n->data = strdup(text);
    if (!n->data) {
        free(n);
        return NULL;
    }
    n->next = NULL;
    return n;
}

void free_list(Node **head) {
    Node *cur = *head;
    while (cur) {
        Node *tmp = cur;
        cur = cur->next;
        free(tmp->data);
        free(tmp);
    }
    *head = NULL;
}

int main(void) {
    Node *head = NULL, *tail = NULL;
    char buffer[256];

    printf("Enter text: ");
    if (fgets(buffer, sizeof(buffer), stdin) == NULL) return 1;
    buffer[strcspn(buffer, "\n")] = '\0';

    Node *n = create_node(buffer);
    if (!n) {
        perror("create_node");
        free_list(&head);
        return 1;
    }
    if (!head) head = n;
    else tail->next = n;
    tail = n;

    // Safely print list
    for (Node *cur = head; cur; cur = cur->next) {
        printf("Node: %s\n", cur->data);
    }

    free_list(&head);
    return 0;
}