#ifndef __SORT
#define __SORT

#include <stdio.h>
#include <stdlib.h>
#include "tab.h"
#include "complex.h"
#include "sort.h"

void swap(TableRow *ar, int a, int b);

void heap_iter(TableRow *ar, int root, int size);

void heap(TableRow *ar, int size);

void sort(TableRow *ar, int size);

#endif