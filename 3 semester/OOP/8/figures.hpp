#ifndef __FIGURES__
#define __FIGURES__

#include <iostream>
#include <vector>
#include <string>
#include <fstream>
#include <memory>
#include <cmath>

#define eps 10e-6
#define inf 10e6

struct Vertex{
	double x,y;
};

double absol(double x){
	if(x >= 0)
		return x;
	else return -x;
}

std::istream &operator>>(std::istream &input, Vertex &c){
    input >> c.x >> c.y;
    return input;
}

class Figure{
public:
	std::vector<Vertex> cords;

	virtual void Print(std::ostream& os) const = 0;
	virtual void Print(std::string& filename) const = 0;
	virtual void Read(std::istream& is) = 0;
	virtual bool check() = 0;
	virtual ~Figure() = default;
};

class Triangle: public Figure{
public:
	Triangle(){
		for(int i = 0; i < 3; ++i){
			cords.push_back({0,0});
		}
	}
	Triangle(Vertex &c1, Vertex &c2, Vertex &c3){
		cords.push_back(c1);
		cords.push_back(c2);
		cords.push_back(c3);
	}

	void Print(std::ostream& os)const override{
		os << "Triangle: ";
		for(int i = 0; i < 3; ++i){
			os << "(" << cords[i].x << " " << cords[i].y << ") ";
		}
		os << std::endl;
	}

	void Print(std::string& filename) const override{
		std::ofstream file;
		file.open(filename);
		if(!file.is_open()){
			std::cout << "File is not open" << std::endl;
			return;
		}
		file << "Triangle: ";
		for(int i = 0; i < 3; ++i){
			file << "(" << cords[i].x << " " << cords[i].y << ") ";
		}
		file.close();
	}

	void Read(std::istream& is){
		for(int i = 0; i < 3; ++i){
			is >> cords[i];
		}
	}

	bool check() override{
		double k1; 
		double k2; 
		if((cords[1].x - cords[0].x) == 0){
			k1 = inf;
		}
		else{
			k1 =  (cords[1].y - cords[0].y)/(cords[1].x - cords[0].x);
		}

		if((cords[2].x - cords[1].x) == 0){
			k2 = inf;
		}
		else{
			k2 = (cords[2].y - cords[1].y)/(cords[2].x - cords[1].x);
		}

		if(absol(k1-k2) < eps)
			return false;

		return true;
	}
};

class Square: public Figure{
public:
	Square(){
		for(int i = 0; i < 4; ++i){
			cords.push_back({0,0});
		}
	}
	Square(Vertex &c1, Vertex &c2, Vertex &c3, Vertex &c4){
		cords.push_back(c1);
		cords.push_back(c2);
		cords.push_back(c3);
		cords.push_back(c4);
	}

	void Print(std::ostream& os)const override{
		os << "Square: ";
		for(int i = 0; i < 4; ++i){
			os << "(" << cords[i].x << " " << cords[i].y << ") ";
		}
		os << std::endl;
	}

	void Print(std::string& filename) const override{
		std::ofstream file;
		file.open(filename);
		if(!file.is_open()){
			std::cout << "File is not open" << std::endl;
			return;
		}
		file << "Square: ";
		for(int i = 0; i < 4; ++i){
			file << "(" << cords[i].x << " " << cords[i].y << ") ";
		}
		file.close();
	}

	void Read(std::istream& is){
		for(int i = 0; i < 4; ++i){
			is >> cords[i];
		}
	}

	bool check() override{
        Vertex v1,v2,v3,v4;
        double l1,l2,l3,l4;

        v1.x = cords[1].x - cords[0].x;
        v1.y = cords[1].y - cords[0].y;
        v2.x = cords[2].x - cords[1].x;
        v2.y = cords[2].y - cords[1].y;
        v3.x = cords[3].x - cords[2].x;
        v3.y = cords[3].y - cords[2].y;
        v4.x = cords[0].x - cords[3].x;
        v4.y = cords[0].y - cords[3].y;

        l1 = v1.x*v1.x + v1.y*v1.y;
        l2 = v2.x*v2.x + v2.y*v2.y;
        l3 = v3.x*v3.x + v3.y*v3.y;
        l4 = v4.x*v4.x + v4.y*v4.y;

        if((l1!=l2) || (l1!=l3) || (l1!=l4) || (l2!=l3) || (l2!=l4) || (l3!=l4))
            return false;

        if( absol(v1.x*v2.x + v1.y*v2.y)>eps || absol(v1.x*v3.x + v1.y*v3.y)<eps || absol(v2.x*v3.x + v2.y*v3.y)>eps ||
            absol(v1.x*v4.x + v1.y*v4.y)>eps || absol(v2.x*v4.x + v2.y*v4.y)<eps || absol(v3.x*v4.x + v3.y*v4.y)>eps)
            return false;
		
		return true;
	}
};

class Rectangle: public Figure{
public:
	Rectangle(){
		for(int i = 0; i < 4; ++i){
			cords.push_back({0,0});
		}
	}
	Rectangle(Vertex &c1, Vertex &c2, Vertex &c3, Vertex &c4){
		cords.push_back(c1);
		cords.push_back(c2);
		cords.push_back(c3);
		cords.push_back(c4);
	}

	void Print(std::ostream& os)const override{
		os << "Rectangle: ";
		for(int i = 0; i < 4; ++i){
			os << "(" << cords[i].x << " " << cords[i].y << ") ";
		}
		os << std::endl;
	}

	void Print(std::string& filename) const override{
		std::ofstream file;
		file.open(filename);
		if(!file.is_open()){
			std::cout << "File is not open" << std::endl;
			return;
		}
		file << "Rectangle: ";
		for(int i = 0; i < 4; ++i){
			file << "(" << cords[i].x << " " << cords[i].y << ") ";
		}
		file.close();
	}

	void Read(std::istream& is){
		for(int i = 0; i < 4; ++i){
			is >> cords[i];
		}
	}

	bool check() override{
        Vertex v1,v2,v3,v4;

        v1.x = cords[1].x - cords[0].x;
        v1.y = cords[1].y - cords[0].y;
        v2.x = cords[2].x - cords[1].x;
        v2.y = cords[2].y - cords[1].y;
        v3.x = cords[3].x - cords[2].x;
        v3.y = cords[3].y - cords[2].y;
        v4.x = cords[0].x - cords[3].x;
        v4.y = cords[0].y - cords[3].y;

        if( absol(v1.x*v2.x + v1.y*v2.y)>eps || absol(v1.x*v3.x + v1.y*v3.y)<eps || absol(v2.x*v3.x + v2.y*v3.y)>eps ||
            absol(v1.x*v4.x + v1.y*v4.y)>eps || absol(v2.x*v4.x + v2.y*v4.y)<eps || absol(v3.x*v4.x + v3.y*v4.y)>eps)
            return false;

		return true;
	}
};

class Factory{
public:
	virtual std::unique_ptr<Figure> create(std::istream& is) = 0;
	virtual std::unique_ptr<Figure> create(std::unique_ptr<Figure> f) = 0;
	virtual ~Factory(){}
};

class TriangleFactory: public Factory{
public:
	std::unique_ptr<Figure> create(std::istream& is)override{
		std::unique_ptr<Triangle> tmp;
		tmp = std::make_unique<Triangle>();
		tmp->Read(is);
		if(tmp->check())
			return std::move(tmp);
		else
			return nullptr;
	}

	std::unique_ptr<Figure> create(std::unique_ptr<Figure> f)override{
		return std::move(f);
	}
};

class SquareFactory: public Factory{
public:
	std::unique_ptr<Figure> create(std::istream& is)override{
		std::unique_ptr<Square> tmp;
		tmp = std::make_unique<Square>();
		tmp->Read(is);
		if(tmp->check())
			return std::move(tmp);
		else
			return nullptr;
	}

	std::unique_ptr<Figure> create(std::unique_ptr<Figure> f)override{
		return std::move(f);
	}
};

class RectangleFactory: public Factory{
public:
	std::unique_ptr<Figure> create(std::istream& is)override{
		std::unique_ptr<Rectangle> tmp;
		tmp = std::make_unique<Rectangle>();
		tmp->Read(is);
		if(tmp->check())
			return std::move(tmp);
		else 
			return nullptr;
	}

	std::unique_ptr<Figure> create(std::unique_ptr<Figure> f)override{
		return std::move(f);
	}
};

#endif