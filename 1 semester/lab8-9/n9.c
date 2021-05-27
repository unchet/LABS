#include <stdio.h>
#include <math.h>
#include <stdlib.h>

#define i0 10
#define j0 20 
#define l0 -1

//Задаем операцию min функцией 
int min(int x, int y) {
	return (x < y) ? x : y;
}

//Задаем операцию max функцией
int max(int x, int y) {
	return (x > y) ? x : y; 
}

//Задаем операцию sign функцией
int sign(int x) {
	if (x>0) return 1;
	if (x<0) return -1;
	return 0; 
}

//Нужная область
int area(int x, int y) {
	return (x<=15 && x>=5 && y<=-5 && y>=-15);
}

//Формула параметра i
int comp_i(int i, int j, int l, int k) {
		int i1 = (fabs(max(i*(k+5), j*(k+6)))-fabs(min(j*(k+7),l*(k+8))));
		int res = i1%20;
		return res;
}

//Формула параметра j
int comp_j(int i, int j, int l, int k) {
		int j1 = (3-sign(i-j))*fabs(min(min(i*l+5,j*l-3),i*j+6));
		int res = j1%25-7;
		return res;
}	
//Формула параметра l	
int comp_l(int i, int j, int l, int k) {
		return i%10+j%10+l%10;	
}	
	
int main() {
	int i, j, l, k, i_old = i0, j_old = j0, l_old = l0;
	
	for (k = 0; k<50; k++) {	
	
		i = comp_i(i_old,j_old,l_old,k);
		j = comp_j(i_old,j_old,l_old,k);
		l = comp_l(i_old,j_old,l_old,k);
		//printf("k=%d, i=%d, j=%d, l=%d\n",k+1,i,j,l);
		i_old = i, j_old = j, l_old = l;
		
			if (area(i,j)) { 
				printf("The point is inside the area\n k = %d, i = %d, j = %d, l = %d\n",k+1,i,j,l);
				break;
			               }
			if (k==49 && !area(i,j))
				printf("No right answer\n");
			  }
return 0;
		  }



