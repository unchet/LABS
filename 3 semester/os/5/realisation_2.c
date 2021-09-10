#include <stdio.h>
#include <math.h>
#include <stdbool.h>
#include <stdlib.h>

float Derivative(float A, float deltaX){
	return (cos(A + deltaX) - cos(A - deltaX))/(2*deltaX);
}

bool deleted(int *arr, int size, int num){
	for(int i = 0; i < size; ++i){
		if(arr[i] == num)
			return true;
	}
	return false;
}

int PrimeCount(int A, int B){
	if(A < 2)
		A = 2;
	int counter = B-A, k = 0;
	int *arr_of_deleted = (int*) malloc(sizeof(int) * (B-A));

	for(int i = A; i <= B; ++i){
		for(int j = i+1; j <= B; ++j){
			if(!(j%i) && !deleted(arr_of_deleted, k, j)){
				arr_of_deleted[k++] = j;
				--counter;
			}
		}
	}
	for(int i = 2; i <= B; ++i){
		if(!deleted(arr_of_deleted, k, i))
			printf("%d", i);
	}
	free(arr_of_deleted);
	return counter+1;
}


