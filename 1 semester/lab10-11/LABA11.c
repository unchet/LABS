#include <stdio.h>
#define space ' '
#define tab '\t'
#define comma ','
#define string '\n'

//Функция для возведения 10 или 5 в нужную степень
int pw(int s,int x)
{
	int a = 1;
	for (; x>0; x--)
		if (s==10)
			a*=10;
		
			else 
				if (s==5)
					a*=5;
	return a;
}

int main()
{
	int quin = 0, test, dec = 0, j = 0, k = 0, minus;
	char i; 
	
	//Основной цикл для считывания символов с текстового файла
returning:	while ((i=getchar())!=EOF)
			{
				if (i=='-')
					minus=1;
					
				if (i>='0' && i<='4')
				{
					quin += (i - '0') * pw(10,j);
					j++;
				}	
				else
					if (i==space || i==tab || i==string)
					{
						if (i==tab || i==string)
							i=space;
						
						if (quin==0)
							goto returning;
						
						test = quin;
						goto changing;
					}
						
					else
						if (i==comma)
						{
							if (quin==0)
							goto returning;
						
							test = quin;
							goto changing;
						}
						
						else
						//Проверка, что число в пятеричной с.с
							if ((i>='5' && i<='9') || (i>='a' && i<='z') || (i>='A' && i<='Z'))
							{
								j = 0;
								quin = 0;
								dec = 0;
								minus = 0;
								//Пропуск всех символов числа не в пятеричной с.с
								while ((i=getchar())!=space)
								{
									if (i==string || i==tab || i==comma)
										goto returning;
									
									if (i==EOF)
										break;
								}
							}
				test = quin;
			}
	
	//Проверка, что число не в троичной с.с
changing:	for (k = 0; test>0; k++)
			{
				if ((test%10)==3 || (test%10)==4)
					break;	
				test /=10;
				if (test==0)
				{
					j = 0;
					dec = 0;
					quin = 0;
					minus = 0;
					goto returning;
				}
			}
	
	//Цикл для перевода числа из пятеричной с.с в десятичную
	for ( ;j>=1; j--)
	{
		dec += (quin%10) * pw(5,j-1);
		quin /= 10;
			
		if (j==1)
		{
			if (minus == 0)
			{
				printf("%d ", dec);
				j = 0;
				dec = 0;
				quin = 0;
				goto returning;
			}
			else
			{
				printf("%d ", (-1*dec));
				j = 0;
				dec = 0;
				quin = 0;
				minus = 0;
				goto returning;
			}
		}
	}
	
printf("\n");

return 0;
}
