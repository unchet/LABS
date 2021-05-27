#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include "stack.h"

void QuickSort(Stack *S){ 
    if(!is_stack_empty(S)){
        Stack *S1, *S2; 
    	int value, value1;  
        S1 = init(); 
        S2 = init();
        value = pop(S);
        while(!is_stack_empty(S)){
            value1 = pop(S);
            if(value1 > value) 
                push(S1, value1);
            else 
                push(S2, value1);
        }
        QuickSort(S1);
        QuickSort(S2);
        push(S2, value);
        append(S1, S2);
        connect(S, S1);
        clear_stack(&S1);
        clear_stack(&S2);
    }

}

int main(){ 
    srand(time(NULL)); 
    Stack *S = NULL;
    int v, random, user_choice = 1;
    S = init(); 
    while(user_choice){ 
   		printf("\n1. Заполнить стек случайными значениями.\n"
               "2. Распечатать стек.\n"
               "3. Вставить в конец.\n"
               "4. Вытащить из конца.\n"
               "5. Посмотреть последний элемент.\n"
               "6. Размер стека.\n"
               "7. Сортировка стека.\n"
               "8. Очистить стек.\n"
               "0. Выход.\n\n");
        printf("Выберите действие: "); 
        scanf("%d",&user_choice);
        printf("\n");
        switch(user_choice){
            case 1:
                printf("Введите количество элементов: "); 
                scanf("%d",&random);
                while(random--) 
                    push(S, rand() % 201 - 100);
                break;
            case 2:
                print_stack(S);
                break;
            case 3:
                if(S == NULL)
                    S = init();
                printf("Введите значение: "); 
                scanf("%d",&v); 
                push(S,v);
                break;
            case 4:
                if(!is_stack_empty(S))
                    printf("Вытащено: %d\n", pop(S));
                else
                    printf("Стек пуст!\n");
                break;
            case 5:
                if(!is_stack_empty(S))
                     printf("Последний элемент = %d\n", end(S));
                else
                    printf("Стек пуст!\n");
                break;
            case 6:
                printf("Размер стека = %d\n", size(S));
                break;
            case 7:
                if(!is_stack_empty(S)){
                    QuickSort(S);
                    printf("Отсортировано!\n");
                }
                else 
                    printf("Стек пуст!\n");
                break;
            case 8:
                if(!is_stack_empty(S)){
                    clear_stack(&S);
                    printf("Стек очищен\n");
                }
                else 
                    printf("Стек уже пуст!\n");
                break;
            case 0:
                printf("Конец\n");
                break;
            default: 
                printf("Неверный номер!\n");
        }
    }
    
    if(S != NULL)
        clear_stack(&S);
    
    return 0;
}
