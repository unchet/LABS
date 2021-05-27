#include <stdio.h>

//Функция для возведения 10 в нужную степень 

int pw(int s,int x)
{
	int a = 1;
	for (; x>0; x--)
		a *= 10;
	return a;
}

//Функция для взятия модуля разности двух соседних цифр
int dif(long a, long b)
{
	if (a>=b) 
		return (a-b);
	else
		return (b-a);
}

int main()
{
	long first_number, second_number = 0;
	int i;
	
	printf("Введите число: ");
	scanf("%ld",&first_number);
	
	//Цикл для образования нового числа
	for (i = 0; first_number>9; i++)
	{
		second_number += dif(first_number%10, ((first_number%100)/10)) * pw(10,i);
		first_number /= 10;
	}
	
	printf("Результат: %ld, %ld\n", second_number, (second_number*3));

	return 0;
}
