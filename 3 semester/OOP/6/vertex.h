#ifndef __VERTEX__
#define __VERTEX__

#include<iostream>

template<class T>
class Vertex {
public:
	T x, y;
};

template<class T>
std::istream& operator>>(std::istream& is, Vertex<T>& point) {
	is >> point.x >> point.y;
	return is;
}

template<class T>
std::ostream& operator<<(std::ostream& os, Vertex<T> point) {
	os << '[' << point.x << ",  " << point.y << ']';
	return os;
}

#endif
