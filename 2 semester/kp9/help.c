#include <stdio.h>
#include <stdlib.h>
#include "tab.h"
#include "complex.h"
#include "sort.h"

int get_size(char *file){
	FILE *f = fopen(file, "rb");
	int64_t size;
	fseek(f, 0L, SEEK_END);
	size = ftell(f);	
	fclose(f);
	return size / sizeof(TableRow);
}

TableRow* find(TableRow *ar, int n, complex key) {
	int l = 0;
	int r = n - 1;
	while (l < r - 1) {
		int m = (l + r) / 2;
		if (less(ar[m].key, key)) {
			l = m;
		} else {
			r = m;
		}
	}
	for (int i = l; i <= r; ++i) {
		if (equal(ar[i].key, key)) {
			return ar + i;
		}
	}
	return NULL;
}

void print_row(TableRow *row){
	printf("%d+%di\t%s\n",row->key.re, row->key.im, row->value);
}


void print_ar(TableRow *ar, int size){
    for(int i = 0; i < size; i++)
        printf("%d+%di\t%s\n", ar[i].key.re, ar[i].key.im, ar[i].value);
    printf("\n");
}

void reverse(TableRow *a, int size){
	for(int i = 0, j = size - 1; i < j; i++, j--){
		TableRow tmp = a[i];
		a[i] = a[j];
		a[j] = tmp;
	}
}

int main(int argc, char **argv){
    if(argc != 2){
		printf("Error. Usage %s <input file>\n",argv[0]);
		return 1;
	}

    FILE *input = fopen(argv[1], "r");
    if(input == NULL){
    	printf("Error. It is impossible to open the input file\n");
		return 1;
	}

	int n, k = 0, user_choice, check = 1;
  	n = get_size(argv[1]);

    TableRow a[n];
    complex value;
    TableRow *row;

    for(int i = 0; i < n; ++i)
		fread(&a[i], sizeof(TableRow), 1, input);
	
	fclose(input);
	while(check){
		printf("\nВыберите действие:\n"
			   "1. Показать таблицу\n"
			   "2. Отсортировать\n"
			   "3. Обратный порядок\n"
			   "4. Бинарный поиск\n"
			   "0. Завершить программу\n");
		check = scanf("%d",&user_choice);
		printf("\n");
	  	switch(user_choice){
	  		case 1:
			    print_ar(a, n);
			    break;
			case 2:
				printf("Было:\n");
				print_ar(a, n);
			    sort(a, n); 
			    printf("Стало:\n");
			    print_ar(a, n);
			    k = 1;
			    break;
			case 3:
				printf("Было:\n");
				print_ar(a, n);
				reverse(a, n);
				printf("Стало:\n");
		    	print_ar(a, n);
		    	k = 0;
		    	break;
		    case 4:
		    	if(k){
			    	print_ar(a, n);
			    	printf("Какой ключ искать?\n");
			    	scanf("%d+%di",&value.re, &value.im);
			    	row = find(a, n, value);
			    	if(row != NULL){
			    		printf("Ключ найден:\n");
			    		print_row(row);
			    	}
			    	else
			    		printf("Ключ не найден\n");
			    } else
			    	printf("Таблица не отсортирована!\n");
		    	break;
		    case 0:
		    	return 0;
		    default:
		    	printf("Неправильная команда!\n");

		}
	}
	return 0;
}