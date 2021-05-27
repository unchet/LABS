#include <stdio.h>
#include <stdlib.h>
#include "tab.h"
#include "complex.h"
#include "sort.h"

void swap(TableRow *ar, int a, int b){ //поменять местами два элемента массива
	TableRow tmp = ar[a];
	ar[a] = ar[b];
	ar[b] = tmp;
}

void heap_iter(TableRow *ar, int root, int size){ //шаг пирамидальной сортировки
	int leftChild = (root * 2) + 1;
	int rightChild = (root * 2) + 2;
	int biggest = root;
	if(leftChild < size && less(ar[root].key, ar[leftChild].key))
		biggest = leftChild;
	if(rightChild < size && less(ar[biggest].key, ar[rightChild].key))
		biggest = rightChild;
	if(biggest != root){
		swap(ar, root, biggest);
		heap_iter(ar, biggest, size);
	}
}

void heap(TableRow *ar, int size){ //1 этап, начало формирования кучи
	for(int i = (size/2)-1; i >= 0 ; i--){
		heap_iter(ar, i, size);		
	}
}

void sort(TableRow *ar, int size){ //сортировка
	heap(ar, size);
	for(int i = size-1; i > 0; i--){
		swap(ar, 0, i);
		heap_iter(ar, 0, i);
	}
}
