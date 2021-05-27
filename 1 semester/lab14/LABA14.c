#include <stdio.h>
#define N 7

int main()
{
	int matrix[N][N], n, i, j, diag = 1;
	
	printf("Введите порядок матрицы: ");
	scanf("%d",&n);
	
	//Проверка условия на порядок
	if (n>7)
	{
		printf("Слишком большая матрица, максимальный порядок равен 7. Выберите другое значение\n");
		return 0;
	}
	
	printf("Матрица:\n");
	
	//Заполнение матрицы
	for (i=0; i<n; i++)
	{
		for (j=0; j<n; j++)
		{
			matrix[i][j] = (i+1)*10+j+1;
			printf("%d ",matrix[i][j]);
		}
		printf("\n");
	}

	printf("Ответ:\n");
	
	//Запись элементов, стоящих на главной диагонали и ниже, в нужном порядке
	for ( ; diag<=n; diag++)
	{
		if (diag%2 == 0) 
		//Запись элементов чётных диагоналей
			for (i=0,j=0 ; i<diag; i++,j++)
				printf("%d ",matrix[n-diag+i][j]);
		else 
		//Запись элементов нечётных диагоналей
			for (i=1,j=1; i<=diag; i++,j++)
				printf("%d ",matrix[n-i][diag-j]);
	}
	
	//Запись элементов, стоящих выше главной диагонали, в нужном порядке
	for (diag -= 2; diag>=1; diag--)
	{
		if (diag%2 == 0)
		//Запись элементов чётных диагоналей
			for (i=0,j=0; i<diag; i++,j++)
				printf("%d ",matrix[i][n-diag+j]);
		else
		//Запись элементов нечётных диагоналей
			for (i=1,j=1; i<=diag; i++,j++)
				printf("%d ",matrix[diag-i][n-j]);
	}
	printf("\n");
	
	return 0;	
}
