#include <stdio.h>
#include "student.h"

int main(){
	
	FILE *input = fopen("RESULT", "r");
	if (input == NULL) {
		printf("Couldn't open file %s!\n", "RESULT");
		return 2;
	}
	
	student buf;
	printf("\nNAME\t\tGENDER\tGROUP\t1SEM\t\t2SEM\n\n");
	while(fread(&buf, sizeof(buf), 1, input)){
		printf("%s\t%c\t%d\t%d %d %d %d \t%d %d %d %d\n", buf.name, buf.gender, buf.group, buf.v11, buf.v12, buf.v13, buf.v14, buf.v21, buf.v22, buf.v23, buf.v24);
	}
	printf("\n");
	
	return 0;
}