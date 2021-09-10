#ifndef __FIGURES__
#define __FIGURES__

#include <iostream>
#include <string.h>
#include <cmath>
#include <tuple>
using namespace std;

template <class T>
class Trapezoid{
public:
	pair<T, T> arr[4];
	string type = "Trapezoid";
};

template <class T>
class Square{
public:
	string type = "Square";
	pair<T, T> arr[4];
};

template <class T>
class Rectangle{
public:
	pair<T, T> arr[4];
	string type = "Rectangle";
};

template <class T>
double calcArea(T& item){
	if (item.type == "Trapezoid"){
		double a = item.arr[3].first - item.arr[0].first;
		double b = item.arr[2].first - item.arr[1].first;
		double h = item.arr[1].second - item.arr[0].second;
		double S = h * 0.5 *(a+b);
		return S;
	}
	double tmp = (item.arr[1].first - item.arr[0].first) + (item.arr[1].second - item.arr[0].second);
	double t = (item.arr[2].first - item.arr[1].first) + (item.arr[2].second - item.arr[1].second);
	return fabs(tmp * t);

}

template <class T, size_t index>
double areaTuple(T& tuple){
    auto item = get<index>(tuple);
    double value = calcArea(item);
    if constexpr ((index+1) <tuple_size<T>::value) {
        return value + areaTuple<T, index + 1>(tuple);
    }

    return value;
}

template <class T>
void displayFigure(T& figure){
		for(auto points: figure.arr){
			cout << "(" << points.first << ", " << points.second << ")";
			cout << " ";
		}
	double S = calcArea(figure);
	cout << "\nArea is " << S << endl << endl;
}

template<class T, size_t idx>
void displayTuple(T& tuple){
	if constexpr(idx < tuple_size<T>::value) {
		auto figure = get<idx>(tuple);
		cout << figure.type << " \t";
		displayFigure(figure);
		displayTuple<T, idx + 1>(tuple);
	}
}

#endif