#ifndef __RECTANGLE__
#define __RECTANGLE__

#include"vertex.h"

template <class T>
class Rectangle {
private:
	Vertex<T> Vertexs[4];
public:
	Rectangle() = default;
	Rectangle(std::istream& in);

	void read(std::istream& in);
	Vertex<T> center() const;
	double square() const;
	void print(std::ostream& os) const;
	bool check() const;
};

template<class T> Rectangle<T>::Rectangle(std::istream& in) {
	for (int i = 0; i < 4; i++)
		in >> Vertexs[i];
}
template<class T> double Rectangle<T>::square() const {
	double Area = 0;
	for (int i = 0; i < 4; i++) {
		Area += (Vertexs[i].x) * (Vertexs[(i + 1) % 4].y) - (Vertexs[(i + 1) % 4].x) * (Vertexs[i].y);
	}
	Area *= 0.5;
	return abs(Area);
}

template<class T> void Rectangle<T>::print(std::ostream& os) const {
	os << "Rectangle: ";
	for (int i = 0; i < 4; i++)

		os << Vertexs[i] << ' ';
	os << '\n';
}

template <class T> void Rectangle<T>::read(std::istream& in) {
	Rectangle<T> res = Rectangle(in);
	*this = res;
}

template<class T>
std::ostream& operator<< (std::ostream& out, const Rectangle<T>& point) {
	out << "Rectangle: ";
	for (int i = 0; i < 4; i++)
		out << point.Vertexs[i] << ' ';
	out << '\n';
	return out;
}

template<class T>
std::istream& operator>> (std::istream& in, const Rectangle<T>& point) {
	for (int i = 0; i < 4; i++)
		in >> point.Vertexs[i];
	return in;
}

template<class T> bool Rectangle<T>::check() const{
	if ((Vertexs[3].x - Vertexs[0].x) == 0 || (Vertexs[2].x - Vertexs[1].x) == 0)
		return false;
	
	double k1 = (Vertexs[3].y - Vertexs[0].y)/(Vertexs[3].x - Vertexs[0].x);
	double b1 = (Vertexs[3].x*Vertexs[0].y - Vertexs[0].x*Vertexs[3].y)/(Vertexs[3].x - Vertexs[0].x);
	double k2 = (Vertexs[2].y - Vertexs[1].y)/(Vertexs[2].x - Vertexs[1].x);
	double b2 = (Vertexs[2].x*Vertexs[1].y - Vertexs[1].x*Vertexs[2].y)/(Vertexs[2].x - Vertexs[1].x);
	double k3 = Vertexs[1].x - Vertexs[0].x;
	double b3;
	if(k3 == 0){
		b3 = Vertexs[1].x;
	}else{
		return false;
	}
	double k4 = Vertexs[3].x - Vertexs[2].x;
	double b4;
	if(k4 == 0){
		b4 = Vertexs[3].x;
	}else{
		return false;
	}


	if((k1 == k2) && (b1 != b2) && (k3 == k4) && (b3 != b4))
		return true;

	return false;
}

#endif