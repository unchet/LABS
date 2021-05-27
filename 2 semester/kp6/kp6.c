// фамилия, инициалы, пол, № группы, оценки за экзамены за два семестра
// вывести имена и количество студенток из групп g1 и g2, средний балл за экзамен которых увеличился более, чем на k (k<=3) баллов
// и найти среди них тех,кто получил хотя бы одну двойку в 1 семестре, а во втором не получили ни одной 
// среди них найти студентку, чей прирост среднего балла наибольший и выяснить, насколько он больше, чем у остальных 

#include <stdio.h>
#include <string.h>
#include "student.h"

double growth(student *stud){
	int v1 = stud->v11 + stud->v12 + stud->v13 + stud->v14;
	int v2 = stud->v21 + stud->v22 + stud->v23 + stud->v24;
	return (v2-v1)/4.0;
}

int find_mark(student *stud){
	if((stud->v11 == 2 || stud->v12 == 2 || stud->v13 == 2 || stud->v14 == 2) &&
	   (stud->v21 != 2 && stud->v22 != 2 && stud->v23 != 2 && stud->v24 != 2))
	   return 1;
	return 0;
}

int main(int argc, char **argv) {
	if (argc < 2) {
		fprintf(stderr, "Error. Usage %s <input file>\n", argv[0]);
		return 1;
	}
	if(argc == 3){
		if (strcmp(argv[2], "-f") == 0) {
			FILE *stream = popen("./write.out","w");
			pclose(stream);
		} else {
			printf("Wrong key! Usage with key %s <input file> -f\n", argv[0]);
			return 1;
		}
	}
	
	FILE *input = fopen(argv[1], "r");
	if (input == NULL) {
		printf("Couldn't open file %s!\n", argv[1]);
		return 2;
	}

	student buf;
	student ans;
	int g1, g2, n = 0;
	double k, mark_growth, max_growth = 0;;
	printf("Введите номера двух групп:\n");
	while(1){
		scanf("%d %d", &g1, &g2);
		if ((g1 > 100 && g2 > 100) && (g1 != g2))
			break;
		printf("Номера групп должны быть трёхзначными и они должны отличаться! Повторите попытку\n");
	}
	printf("Введите значение, на которое как минимум увеличилась средняя оценка:\n");
	while(1){
		scanf("%lf",&k);
		if(k <= 3)
			break;
		printf("Вы ввели неправильное значение! Повторите попытку\n");
	}

	while (fread(&buf, sizeof(student), 1, input)) {
		if (buf.gender == 'F' && (buf.group == g1 || buf.group == g2)){
			mark_growth = growth(&buf);
			if(mark_growth >= k){
				if(mark_growth > max_growth){
					max_growth = mark_growth;
					ans = buf;
				}
				printf("\n> Студентка %s из %d группы увеличила свой средний балл на %.2lf. ", buf.name, buf.group, mark_growth);
				if(find_mark(&buf))
					printf("В первом семестре у неё были \"двойки\", а во втором ни одной");
				printf("\n");
				n++;
			}
		}
	}
	
	printf("\nКоличество найденных студенток: %d\n",n);

	if(max_growth){
		fseek(input, 0, SEEK_SET);
		printf("\nСтудентка %s из %d группы имеет максимальный прирост оценки в %.2lf баллов среди групп %d и %d\n", ans.name, ans.group, max_growth, g1, g2);
		while (fread(&buf, sizeof(student), 1, input)) {
			if (strcmp(buf.name, ans.name) == 0)
				continue;
			if (buf.gender != 'F' || (buf.group != g1 && buf.group !=g2) || growth(&buf) < k)
				continue;
			if (max_growth == growth(&buf))
				continue;
			printf("\t> Это больше на %.2lf чем у студентки %s из %d группы\n", max_growth - growth(&buf), buf.name, buf.group);
		}
	} else printf("Таких студенток нет\n");
	
	fclose(input);
	return 0;
}