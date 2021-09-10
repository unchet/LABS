#include <stdio.h>
#include <stdlib.h>
#include <dlfcn.h>
#include <stdbool.h>

const char *FirstRealLib = "./libs/lib1.so";
const char *SecondRealLib = "./libs/lib2.so";

int main(){
	int current = 1;
	void *lib = dlopen(FirstRealLib, RTLD_LAZY);
	if(!lib){
		perror("Error with openning lib");
		exit(1);
	}

	float (*Derivative) (float, float);
	int (*PrimeCount) (int, int);

	*(void**) (&Derivative) = dlsym(lib, "Derivative");
	char *error = dlerror();
	if(error!=NULL){
		perror("Error with Derivative");
		exit(1);
	}

	*(void**) (&PrimeCount) = dlsym(lib, "PrimeCount");
	error = dlerror();
	if(error!=NULL){
		perror("Error with PrimeCount");
		exit(1);
	}

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
		else if(!arguments){
			if(dlclose(lib)){
				perror("Can't close lib");
				exit(1);
			}
			if(current == 1){
				current = 2;
				lib = dlopen(SecondRealLib, RTLD_LAZY);
			}
			else{
				current = 1;
				lib = dlopen(FirstRealLib, RTLD_LAZY);
			}

			if(!lib){
				printf("Error opening library\n");
				return 1;
			}

			*(void**) (&Derivative) = dlsym(lib, "Derivative");
			*(void**) (&PrimeCount) = dlsym(lib, "PrimeCount");
			error = dlerror();
			if(error != NULL){
				printf("Error with func\n");
				return 1;
			}
			printf("Realisation is swapped!\n");
		}
		else{
			printf("Wrong format! Try again\n");
			continue;
		}
	}

	return 0;
}