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
	int counter = 0;
	if(A < 2)
		A = 2;

	for(int i = A; i <= B; ++i){
		if(is_prime(i)){
			printf("%d\n", i);
			++counter;
		}
	}
	return counter;
}

