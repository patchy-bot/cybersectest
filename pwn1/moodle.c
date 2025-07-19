#include <stdio.h>
#include <unistd.h>
#include <string.h>

int main() {
    printf("The graph of the polynomial function f(x) = -2x^4-16x^3-49x^2-68x-33 is symmetric with respect to a vertical line. Find the equation of this vertical line:\nx= \n");
    
    char secret[] = "cmxw    m{ft    ld00    4m_3    r3t5    dn1m    }!!!    ";

    char name[1000] = {0};
    
    read(0, name, 1000);
    printf(name);
    if (strcmp(name, "3\n")==0) {
    	printf("\nCorrect!");
    } else {
    	printf("\nIncorrect!");
    }
    return 0;
}

