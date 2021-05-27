#include <stdio.h>
#include "set.h"
#include <ctype.h>

char word1[20], word2[20], S1[2*N], Scheck[2*N], S2[2*N];

//Функция для копирования множеств
int Copy (char S1[],char S2[])
{
	for (int i=0; i<2*N; i++)
		S2[i]=S1[i];
}

//Функция для опустошения слова
int GoToVoid(char S[])
{
	for (int i=0; i<=20; i++)
		S[i]='\0';
}

//Функция для обнуления множества
int SetToZero(char S[])
{
	for (int i=0; i<=2*N; i++)
		S[i] = '0';
}

int main ()
{
	int i, n = 0, exist = 0;
	char c;
	
	for (int j=0; j<=2*N; j++)
		Scheck[j]='0';

	while ((i=getchar())!=EOF)
	{
		c = i;
		if (Letter(c))
			if (EmptySet(S1))
				while(1)
				{
				word1[n]=c;
				break;
				}
			else
			{
				if (word2[0]=='\0')
					n = 0;
				while(1)
				{
				word2[n]=c;
				break;
				}
			}
		c = tolower(c);

		if (Letter(c))
			InSet(c, Scheck);
		
		else 
			
			if (EmptySet(S1))
			{
				Copy(Scheck, S1);
				SetToZero(Scheck);
				continue;
			}
			
			else	
			{
				Copy(Scheck, S2);
				SetToZero(Scheck);
			}
		
		if (!EmptySet(S1) && !EmptySet(S2))
			{
				if (EqualSet(S1, S2))
				{
					if (!exist)
					{
						printf("Существуют соседние слова, которые состоят из одного набора букв:\n");
						exist=1;
					}
					printf("%s, %s\n", word1, word2);
				}
				
				else 
					for (int j=0; S2[j]!=0; j++)
						S1[j] = S2[j];
				
				for (int j=0; j<=20; j++)
					word1[j] = word2[j];
				
				GoToVoid(word2);
				
				SetToZero(S2);
			}
		n++;
	}
	if (!exist)
		printf("Соседних слов, которые состоят из одного набора букв, не существует\n");
	
	return 0;
}	
