#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define N 8

int main()
{
	int matrix[N][N], line[N*N], i, j, n, k=0, first, number, side;
	
	printf("Введите порядок матрицы: ");
	scanf("%d", &n);
	
	srand(time(0));
	
	while (n>8 || n<1)
	{
		printf("Повторите попытку. Порядок не должен быть меньше единицы и больше восьми.\n\n");
		printf("Введите порядок матрицы: ");
		scanf("%d", &n);
		printf("\n");			
	}
		
	for (i=0; i<n; i++)
		for (j=0; j<n; j++)
			matrix[i][j] = rand()%50;
		
	printf("Матрица:\n\n");
	
	for (i=0; i<n; i++)
	{
		for (j=0; j<n; j++)
			printf("%6d",matrix[i][j]);
		printf("\n\n");
	}
	
	k = 0;
	
	for (i=0; i<n; i++)
		for (j=0; j<n; j++)
		{
			line[k] = matrix[i][j];
			k++;	
		}
			
	printf("Введите число сдвигов: ");
	scanf("%d", &number);
	
	printf("Куда сдвигать? (1-влево, 0-вправо): ");
	scanf("%d", &side);
	printf("\n");

	while (side!=0 && side!=1)
	{
		printf("Повторите попытку. Введите или 1, или 0\n\n");
		printf("Куда сдвигать? (1-влево, 0-вправо): ");
		scanf("%d", &side);
		printf("\n");
	}
	
	if(side)
	{
		while (number>0)
		{
			first = line[0];
			for (k=0; k<n*n; k++)
				line[k] = line[k+1];
			line[n*n-1] = first;
			number--;
		}
	}	
	else
	{
		while (number>0)
		{
			first = line[n*n-1];
			for (k=n*n-1; k>0; k--)
				line[k] = line[k-1];
			line[0] = first;
			number--;
		}
	}		
	
	k = 0;
	
	for (i=0; i<n; i++)
		for (j=0; j<n; j++)
		{
			matrix[i][j] = line[k];
			k++;
		}
		
	printf("Результат:\n\n");
	
	for (i=0; i<n; i++)
	{
		for (j=0; j<n; j++)
			printf("%6d",matrix[i][j]);
		printf("\n\n");
	}
	
	return 0;
}