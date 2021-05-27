#include <stdbool.h>
#include <math.h>
#include "complex.h"
#include "tab.h"

bool less(complex a, complex b){
	return sqrt(a.re*a.re + a.im*a.im) < sqrt(b.re*b.re + b.im*b.im); 
}

bool equal(complex a, complex b) {
	return (a.re == b.re && a.im == b.im);
}
