#include <stdio.h>
#include <stdlib.h>
#include "sum.c"
int main(void){
    int x;
    printf("Input an integer:\n");
    scanf("%d", &x);
    printf("sum=%d\n", sum(x));
    return 0;
};