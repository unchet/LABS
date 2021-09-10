#include <stdio.h>
#include <math.h>
#include <stdbool.h>

float Derivative(float A, float deltaX){
	return (cos(A + deltaX) - cos(A))/deltaX;
}

bool is_prime(int A){
	for(int i = 2; i < A; ++i){
		if(!(A%i))
			return false;
	}
	return true;
}

int PrimeCount(int A, int B){
	if(A > B){
		printf("Wrong segment!\n");
		return 0;
	}
	int counter = 0;
	if(A < 2)
		A = 2;

	for(int i = A; i <= B; ++i){
		if(is_prime(i)){
			if(!counter)
				printf("Native algorithm:\n");
			printf("%d ", i);
			++counter;
		}
	}
	return counter;
}
