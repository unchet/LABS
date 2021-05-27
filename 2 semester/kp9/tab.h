#ifndef __TAB
#define __TAB
#include <stdbool.h>
#include "complex.h"

typedef struct {
	complex key;
	char value[80];
} TableRow;

bool less(complex a, complex b);

bool equal(complex a, complex b);

#endif