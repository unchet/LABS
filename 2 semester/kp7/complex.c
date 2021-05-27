#include "complex.h"

complex makeComplex(int re, int im) {
	complex c;
	c.re = re;
	c.im = im;
	return c;
}

complex sum(complex a, complex b) {
	complex c;
	c.re = a.re + b.re;
	c.im = a.im + b.im;
	return c;
}

complex substract(complex a, complex b) {
	complex c;
	c.re = a.re - b.re;
	c.im = a.im - b.im;
	return c;
}

complex mult(complex a, complex b) {
	complex c;
	c.re = a.re * b.re - a.im * b.im;
	c.im = a.im * b.re + a.re * b.im;
	return c;
}

complex divide(complex a, complex b) {
	complex tmp = b;
	tmp.im *= -1;
	complex c = mult(a, tmp);
	double znam = b.re * b.re + b.im * b.im;
	c.re /= znam;
	c.im /= znam;
	return c;
}
