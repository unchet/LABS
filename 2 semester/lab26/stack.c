#define N 10
#include "stack.h"
#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>

Stack* init(){
    Stack *S = malloc(sizeof(*S));
    S->max_size = N;
    S->body = malloc(N * sizeof(S->body));
    S->last = 0;
    return S; 
}

bool is_stack_empty(Stack *S){
    if(S == NULL)
        return true;
    return S->last == 0;
}

void resize(Stack *S, int new_size){
    S->max_size = new_size;
    S->body = realloc(S->body, new_size * sizeof(S->body));
}

void push(Stack *S, int value){
    if(S->last == S->max_size) 
        resize(S, (3 * S->max_size) / 2);
  
    S->body[S->last++] = value;
}

int pop(Stack *S){ 
    return S->body[--S->last];
}

int end(Stack *S){  
    return S->body[S->last - 1];
}

int size(Stack *S){
    if(S == NULL)
        return 0;
    return S->last;
}


void print_stack(Stack *S){
    printf("[ ");
    if(S != NULL)
        for(int i = 0; i < S->last; i++) 
            printf("%d ", S->body[i]);
    
    printf("]\n");
}

void clear_stack(Stack **S){
    free((*S)->body);
    free((*S));
    *S = NULL;
}

void connect(Stack *S1, Stack *S2){
    int val;
    if(!is_stack_empty(S2)){ 
        val = pop(S2); 
        connect(S1, S2); 
        push(S1, val);
    }
}

void append(Stack *S1, Stack *S2){ 
    int val;
    if(is_stack_empty(S1)) 
        connect(S1, S2);
    else { 
        val = pop(S1);
        append(S1, S2);
        push(S1, val);
    }
}
