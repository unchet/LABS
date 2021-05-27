#include <stdio.h>
#include <stdlib.h>
#include "complex.h"

typedef struct {
	vectorDataType data[100];
	int sz;
} vector;

void vectorInit(vector *v) {
	v->sz = 0;
}

void push_data(vector *v, complex value) {
	v->data[v->sz++].comp = value;
}

void push_columns(vector *v, int value){
	v->data[v->sz].comp.im = 0;
	v->data[v->sz++].integer = value;
}

complex get_by_idx(vector *v, int idx){
	if(idx < 0 || idx >= v->sz){
		printf("Wrong index\n");
		exit(1);
	}
	return v->data[idx].comp;
}

int get_size(vector *v){
	return v->sz;
}

int max_number(int *ar, int size){
	int max = 0, number, prev_number = -1;
	for(int i = 0; i < size; i++){
		if (ar[i] > max){
			max = ar[i];
			number = i;
		}
		if (ar[i] == max){
			prev_number = number;
			number = i;
		}
	}
	if(prev_number > -1)
		return prev_number;
	return number;
}

int find_column(vector *v, vector *strIdx, int columns){
	int column[columns];
	for(int i = 0; i < columns; i++)
		column[i] = 0;
	for(int i = 0; i < strIdx->sz; i++){
		int num = strIdx->data[i].integer;
		if(num == -1)
			continue;
		while(v->data[num].integer != -1){
			column[v->data[num].integer]++;
			num += 2;
		}
	}
	return max_number(column, columns);
}

complex mult_elem_of_column(complex *elements, int size){
	complex tmp = elements[0];
	for(int i = 1; i < size; i++){
		tmp = mult(tmp, elements[i]);
	}
	return tmp;
}

complex find_elem_of_column(vector *v, vector *strIdx, int number_of_column){
	complex res[strIdx->sz];
	int counter = 0;
	for(int i = 0; i < strIdx->sz; i++){
		res[i].re = 0;
		res[i].im = 0;
	}
	
	for(int i = 0; i < strIdx->sz; i++){
		int num = strIdx->data[i].integer;
		if(num == -1)
			continue;
		while(v->data[num].integer != number_of_column){
			num += 2;
			if(num > v->sz - 2 || v->data[num].integer == -1)
				break;
		}
		if(num > v->sz - 2 || v->data[num].integer == -1)
			continue;
		res[counter] = v->data[num+1].comp;
		counter++;
	}
	return mult_elem_of_column(res, counter);
}

int main() {
	int n, m, column;
	complex test;
	scanf("%d %d", &n, &m);
	vector strIdx;
	vectorInit(&strIdx);
	vector v;
	vectorInit(&v);
	printf("Исходная матрица:\n\n");
	for (int i = 0; i < n; ++i) {
		int flag = 1;
		for (int j = 0; j < m; ++j) {
			complex value;
			scanf("%d+%di", &value.re, &value.im);
			printf("%d+%di ", value.re, value.im);
			if (value.re == 0 && value.im == 0) continue;
			if (flag) {
				flag = 0;
				push_columns(&strIdx, v.sz);
			}
			push_columns(&v, j);
			push_data(&v, value);
		}
		printf("\n");
		if (flag == 0) {
			push_columns(&v, -1);
		} else {
			push_columns(&strIdx, -1);
		}
	}
	printf("\nМатрица в виде цепочки ненулевых элементов в векторе со строчным индексированием:\n\n");
	for(int i = 0; i < n; i++ ){
		printf("%d ",strIdx.data[i].integer);
	}
	printf("\n\n");
	for(int i = 0; i < v.sz; i++ ){
		if(v.data[i].comp.im == 0)
			printf("%d ", v.data[i].integer);
		else
			printf("%d+%di ",v.data[i].comp.re, v.data[i].comp.im);
	}
	printf("\n\n");
	column = find_column(&v, &strIdx, m);
	printf("Столбец с максимальным количеством ненулевых элементов: %d\n", column + 1);
	test = find_elem_of_column(&v, &strIdx, column);
	printf("Результат перемножения всех ненулевых элементов %d столбца: %d+%di\n", column + 1, test.re, test.im);
	
	return 0;
}
