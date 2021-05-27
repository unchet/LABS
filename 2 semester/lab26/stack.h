#ifndef __STACK
#define __STACK
#include <stdbool.h>

typedef struct Stack{ 
	int last;
	int *body;
	int max_size;
} Stack;

Stack* init();

bool is_stack_empty(Stack *S);

void resize(Stack *S, int new_size);

void push(Stack *S, int value);

int pop(Stack *S);

int end(Stack *S);

int size(Stack *S);

void print_stack(Stack *S);

void clear_stack(Stack **S);

void connect(Stack *S1, Stack *S2);

void append(Stack *S1, Stack *S2);

#endif
