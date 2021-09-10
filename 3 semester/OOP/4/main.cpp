#include <iostream>
#include <tuple>
#include "figures.h"


int main(){

	Square<double> sq1;
	sq1.arr[0] = {1.6, 2.8};
	sq1.arr[1] = {1.6, 4.1};
	sq1.arr[2] = {2.9, 4.1};
	sq1.arr[3] = {2.9, 2.8};

	Square<int> sq2;
	sq2.arr[0] = {-1, -1};
	sq2.arr[1] = {-1, 1};
	sq2.arr[2] = {1, 1};
	sq2.arr[3] = {1, -1};

	Rectangle<int> rect1;
	rect1.arr[0] = {-1, 0};
	rect1.arr[1] = {-1, 7};
	rect1.arr[2] = {2, 7};
	rect1.arr[3] = {2, 0};
	
	Rectangle<double> rect2;
	rect2.arr[0] = {-3.5, 1};
	rect2.arr[1] = {-3.5, 2};
	rect2.arr[2] = {4.5, 2};
	rect2.arr[3] = {4.5, 1};

	Trapezoid<double> tr1;
	tr1.arr[0] = {0, 0};
	tr1.arr[1] = {2.5, 4};
	tr1.arr[2] = {6, 4};
	tr1.arr[3] = {8, 0};

	Trapezoid<int> tr2;
	tr2.arr[0] = {-5, -1};
	tr2.arr[1] = {0, 4};
	tr2.arr[2] = {4, 4};
	tr2.arr[3] = {5, -1};

	tuple<decltype(sq1),decltype(sq2),decltype(rect1),decltype(rect2),decltype(tr1),decltype(tr2)> tup{sq1,sq2,rect1,rect2,tr1,tr2};
	cout << "Summ of areas " << areaTuple<decltype(tup),0>(tup) << endl;
	displayTuple<decltype(tup),0>(tup);

	return 0;
}