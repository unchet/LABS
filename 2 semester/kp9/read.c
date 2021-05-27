#include <stdio.h>
#include "tab.h"

int main(int argc, char **argv) {
	if (argc != 3) {
		fprintf(stderr, "Error. Usage %s <input file> <output file>\n", argv[0]);
		return 1;
	}
	FILE *input = fopen(argv[1], "r");
	if (input == NULL) {
		printf("Couldn't open file %s!\n", argv[1]);
		return 1;
	}
	FILE *output = fopen(argv[2], "w");
	if (output == NULL) {
		printf("Couldn't open file %s!\n", argv[2]);
		return 1;
	}
	TableRow buf;
	while (-1 != fscanf(input, "%d+%di\t%[^\n]\n", &buf.key.re, &buf.key.im, buf.value)) {
		fwrite(&buf, sizeof(TableRow), 1, output);
	}
	fclose(input);
	fclose(output);
}