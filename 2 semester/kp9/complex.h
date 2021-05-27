#ifndef __COMPLEX
#define __COMPLEX

typedef struct {
	int re, im;
} complex;

complex makeComplex(int re, int im);

complex sum(complex a, complex b);

complex substract(complex a, complex b);

complex mult(complex a, complex b);

complex divide(complex a, complex b);

typedef union {
	int integer;
	complex comp;
} vectorDataType;

#endif
