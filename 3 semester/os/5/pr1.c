#include <stdio.h>
#include "realisation.h"

int main(){
	int arguments;

	while(scanf("%d",&arguments) > 0){
		if(arguments == 1){
			float A, deltaX = 0.001;
			scanf("%f",&A);
			printf("The result is: %f\n", Derivative(A, deltaX));
		}
		else if(arguments == 2){
			float A, B;
			scanf("%f %f",&A, &B);
			printf("\nIn this segment %d prime numbers\n", PrimeCount(A, B));
		}
		else{
			printf("Wrong format! Try again\n");
			continue;
		}
	}

	return 0;
}