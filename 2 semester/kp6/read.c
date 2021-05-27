#include <stdio.h>

#include "student.h"

int main(int argc, char **argv) {
	if (argc != 2) {
		fprintf(stderr, "Error. Usage %s <input file>\n", argv[0]);
		return 1;
	}
	FILE *input = fopen(argv[1], "r");
	if (input == NULL) {
		printf("Couldn't open file %s!\n", argv[1]);
		return 1;
	}
	FILE *output = fopen("RESULT", "w");

	student buf;
	while (-1 != fscanf(input, "%[^\t]\t%c\t%d\t%d %d %d %d\t%d %d %d %d\n", buf.name, &buf.gender, &buf.group, &buf.v11, &buf.v12, &buf.v13, &buf.v14, &buf.v21, &buf.v22, &buf.v23, &buf.v24)) {
		fwrite(&buf, sizeof(student), 1, output);
	}
	fclose(input);
	fclose(output);
}