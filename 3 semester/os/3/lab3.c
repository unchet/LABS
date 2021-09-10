/*
Отсортировать массив целых чисел при помощи TimSort при 
помощи заданного количества потоков
*/

#include <pthread.h>
#include <stdlib.h>
#include <mcheck.h>
#include <fcntl.h>
#include <stdio.h>
#include <errno.h>
#include <time.h>

#define N 10

int *arr, counter = 1;

typedef struct {
	int l,r, thr;
}arguments;

void init_arr(){
	arr = malloc(N * sizeof(int));
}

arguments* init(){
	arguments *arg = malloc(sizeof(arguments));
	arg->l = 0;
	arg->r = 0;
	arg->thr = 0;
	return arg;
}

int min(int a, int b){
	if(a<=b)
		return a;
	return b;
}

void* insertionSort(void *data) { 
	arguments *arg = (arguments*) data;
	int l = arg->l, r = arg->r;
	for (int i = l + 1; i <= r; ++i){ 
		int temp = arr[i]; 
		int j = i - 1; 
		while (j >= l && arr[j] > temp){ 
			arr[j+1] = arr[j]; 
			j--; 
		} 
		arr[j+1] = temp; 
	}
	return NULL;
}

void* merge(void *data) { 
	arguments *arg = (arguments*) data;
	while(counter != arg->thr);

	int r = arg->r, m = arg->l - 1;
	int len1 = m + 1, len2 = r - arg->l + 1; 
	int left[len1], right[len2]; 
	for (int i = 0; i < len1; i++) 
		left[i] = arr[i]; 
	for (int i = 0; i < len2; i++) 
		right[i] = arr[m + 1 + i]; 
  
	int i = 0, j = 0, k = 0; 

	while (i < len1 && j < len2){ 
		if (left[i] <= right[j]){ 
			arr[k] = left[i]; 
			i++; 
		} 
		else{ 
			arr[k] = right[j]; 
			j++; 
		} 
		k++; 
	} 

	while (i < len1){ 
		arr[k] = left[i]; 
		k++; 
		i++; 
	} 

	while (j < len2){ 
		arr[k] = right[j]; 
		k++; 
		j++; 
	} 
	counter++;
} 

void printAr(int size){
	printf("[ ");
	for(int i = 0; i < size; ++i)
		printf("%d ", arr[i]);
	printf("]\n");
}

void resize(int cap){
	arr = realloc(arr, 2*cap*sizeof(int));
}

int main(int argc, char **argv){
	if(argc != 2){
		printf("Error. Usage %s <number of threads>\n", argv[0]);
		exit(1);
	}
	srand(time(NULL));

	int action = 1, number, i = 0, status, r;
	int cap = N, num_of_threads = atoi(argv[1]);

	pthread_t *threads = malloc(sizeof(pthread_t) * num_of_threads);
	arguments *args = malloc(sizeof(arguments) * num_of_threads);

	init_arr();
	while(action){
		printf("1. Add number\n2. Add random numbers\n3. Print array\n4. Sort\n0. Exit\n");
		scanf("%d",&action);
		switch(action){
			case 1:
				printf("Input number\n");
				scanf("%d",&number);
				if(i == cap){
					resize(cap);
					cap*=2;
				}
				arr[i] = number;
				++i;
				break;
			case 2:
				printf("Write quantity of numbers\n");
				scanf("%d",&r);
				while(r--){
					if(i == cap){
						resize(cap);
						cap*=2;
					}
					arr[i] = 30 - rand()%51;
					++i;
				}
				break;
			case 3:
				printAr(i);
				break;
			case 4:{
				if(counter != 1)
					counter = 1;
				long double begin, end;
				if(i < num_of_threads){
					printf("It's too much threads\n");
					exit(1);
				} 
				int step = i / num_of_threads;
				while(step*num_of_threads < i){
					++step;
				}
				int l = 0, r = step-1;
				int parts = 0;
				for(int k = 0; k < num_of_threads, l < i-1; ++k, l+=step, r+=step){
					args[k].l = l;
					if(r+1 == i-1){
						args[k].r = i-1;
					}
					else{
						args[k].r = min(r, i-1);
					}
					++parts;
					args[k].thr = k;
				}
				begin = clock();
				for(int k = 0; k < parts; ++k){
					if(pthread_create(&threads[k], NULL, insertionSort, &args[k])){
						perror("Can't create thread");
						exit(errno);
					}
				}

				for(int k = 0; k < parts; ++k){
					pthread_join(threads[k], NULL);
				}

				for(int k = 0; k < parts-1; ++k){
					if(pthread_create(&threads[k], NULL, merge, &args[k+1])){
						perror("Can't create thread");
						exit(errno);
					}
				}

				for(int k = 0; k < parts-1; ++k){
					pthread_join(threads[k], NULL);
				}
				end = clock();
				printf("\nExecution time: %Lf ms\n", (end - begin) / 1000.0);
				break;
			}
			case 0:
				action = 0;
				break;
		}
	}

	free(threads);
	free(args);
	free(arr);
	return 0;
}
