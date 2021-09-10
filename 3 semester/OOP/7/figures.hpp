#ifndef _FIGURES_HPP_
#define _FIGURES_HPP_

#include <iostream>
#include <vector>
#include <cmath>

struct Coordinations{
    double x, y;
};

std::istream &operator>>(std::istream &input, Coordinations &c){
    input >> c.x >> c.y;
    return input;
}

std::istream &operator>>(std::istream &input, std::vector<Coordinations> &v){
    for(size_t i = 0; i < v.size(); i++){
        std::cin >> v[i];
    }
    return input;
}

std::ostream &operator<<(std::ostream &output, Coordinations c){
    output << "(" << c.x << " " << c.y << ")";
    return output;
}

bool operator!=(Coordinations c1, Coordinations c2){
    return (c1.x != c2.x || c1.y != c2.y);
}

class Figure{
public:
    std::vector<Coordinations> cords;
    
    Figure(){}
    Figure(const Figure &f){
        for(size_t i = 0; i < f.cords.size(); i++){
            cords.push_back(f.cords[i]);
        }
    }
    virtual ~Figure(){}

    void read_cords(){
        for(size_t i = 0; i < cords.size(); i++){
            std::cin >> cords[i];
        }
    }
    
    virtual void print_name() = 0;
    virtual char get_figure() = 0;

    void print(){
        print_name();
        for(size_t i = 0; i < cords.size(); i++){
            std::cout << cords[i] << " ";
        }
        std::cout << '\n';
    }
};

class Rombus: public Figure{
public:
    Rombus(){
        for(size_t i = 0; i < 4; i++){
            cords.push_back({0, 0});
        }
    }
    Rombus(const Coordinations &c1, const Coordinations &c2, const Coordinations &c3, const Coordinations &c4){
        if (c1 != c2 && c1 != c3 && c1 != c4 &&
            c2 != c3 && c2 != c4 && c3 != c4){
            cords.push_back(c1);
            cords.push_back(c2);
            cords.push_back(c3);
            cords.push_back(c4);
        }
    }
    Rombus(const Rombus &s){
        cords = s.cords;
    }
    Rombus(const std::vector<Coordinations> &v){
        cords = v;
    }
    ~Rombus(){}

    void print_name(){
        std::cout << "Rombus: ";
    }

    char get_figure(){
        return 'r';
    }
    
};


Coordinations get_coordinates(Coordinations &center, double radius, Coordinations &c1, double num){
    double phi1, phi2;
    if(c1.x > 0 && c1.y > 0){
        phi1 = acos(c1.x/radius);
    }
    else if(c1.x < 0 && c1.y > 0){
        phi1 = 4*atan(1) - acos(c1.x/radius);
    }
    else if(c1.x < 0 && c1.y < 0){
        phi1 = 4*atan(1) + acos(c1.x/radius);
    }
    else{
        phi1 = -acos(c1.x/radius);
    }
   
    if(c1.x < 0){
        phi2 = -phi1;
    }
    else {
        phi2 = phi1 + num*4*atan(1)/180;
    }

    Coordinations c2;
    c2.x = radius * cos(phi2);
    c2.y = radius * sin(phi2);

    return c2;
}


class Pentagon: public Figure{
public:
    Pentagon(){
        for(size_t i = 0; i < 5; i++){
            cords.push_back({0,0});
        }
    }

    Pentagon(const Coordinations &c1, const Coordinations &c2, const Coordinations &c3, const Coordinations &c4, const Coordinations &c5){
        if (c1 != c2 && c1 != c3 && c1 != c4 && c1 != c5 &&
            c2 != c3 && c2 != c4 && c2 != c5 && c3 != c4 &&
            c3 != c5 && c4 != c5){
            cords.push_back(c1);
            cords.push_back(c2);
            cords.push_back(c3);
            cords.push_back(c4);
            cords.push_back(c5);
        }
    }
    Pentagon(Coordinations &center, double radius, Coordinations c1){
        Coordinations c2, c3, c4, c5;
        c2 = get_coordinates(center, radius, c1, 72);
        c3 = get_coordinates(center, radius, c2, 72);
        c4 = get_coordinates(center, radius, c3, 72);
        c5 = get_coordinates(center, radius, c4, 72);
        cords.push_back(c1);
        cords.push_back(c2);
        cords.push_back(c3);
        cords.push_back(c4);
        cords.push_back(c5);
    }
    Pentagon(const Pentagon &r){
        cords = r.cords;
    }
    Pentagon(const std::vector<Coordinations> &v){
        cords = v;
    }
    ~Pentagon(){}

    void print_name(){
        std::cout << "Pentagon: ";
    }

    char get_figure(){
        return 'p';
    }
};

class Hexagon: public Figure{
public:
    Hexagon(){
        for(size_t i = 0; i < 4; i++){
            cords.push_back({0,0});
        }
    }
    Hexagon(Coordinations &center, double radius, Coordinations c1){
        Coordinations c2, c3, c4, c5,c6;
        c2 = get_coordinates(center, radius, c1,60);
        c3 = get_coordinates(center, radius, c2,60);
        c4 = get_coordinates(center, radius, c3,60);
        c5 = get_coordinates(center, radius, c4,60);
        c6 = get_coordinates(center, radius, c5,60);
        cords.push_back(c1);
        cords.push_back(c2);
        cords.push_back(c3);
        cords.push_back(c4);
        cords.push_back(c5);
        cords.push_back(c6);
    }
    Hexagon(const Coordinations &c1, const Coordinations &c2, const Coordinations &c3, const Coordinations &c4, const Coordinations &c5, const Coordinations &c6){
        if (c1 != c2 && c1 != c3 && c1 != c4 && c1 != c5 && c1 != c6 &&
            c2 != c3 && c2 != c4 && c2 != c5 && c2 != c6 && c3 != c4 &&
            c3 != c5 && c3 != c6 && c4 != c5 && c4 != c6 && c5 != c6){
            cords.push_back(c1);
            cords.push_back(c2);
            cords.push_back(c3);
            cords.push_back(c4);
            cords.push_back(c5);
            cords.push_back(c6);
        }
    }
    Hexagon(const Hexagon &t){
        cords = t.cords;
    }
    Hexagon(const std::vector<Coordinations> &v){
        cords = v;
    }
    ~Hexagon(){}
    
    void print_name(){
        std::cout << "Hexagon: ";
    }

    char get_figure(){
        return 'h';
    }
};

bool check(const Coordinations &c1, const Coordinations &c2, const Coordinations &c3, const Coordinations &c4){
    
    double k1_chisl = c3.y - c1.y;
    double k1_znam = c3.x - c1.x;
    double k2_chisl = c4.y - c2.y;
    double k2_znam = c4.x - c2.x;
    double res1 = 0, res2 = 0;

    if(k2_znam != 0){
        res1 = k1_chisl / k2_znam;
    }
    if(k1_znam != 0){
        res2 = k2_chisl / k1_znam;
    }

    if(res1*res2 == -1)
        return true;

    if((k2_znam == 0 && k1_chisl == 0) || (k1_znam == 0 && k2_chisl == 0))
        return true;

    return false;
}

class Factory{
public:
    virtual Figure *create() = 0;
    virtual ~Factory(){}
};

class Rombus_Factory: public Factory{
public:
    Figure *create(){
        return reinterpret_cast<Figure*>(new Rombus());
    }
    Figure *create(const Coordinations &c1, const Coordinations &c2, const Coordinations &c3, const Coordinations &c4){
        return reinterpret_cast<Figure*>(new Rombus(c1, c2, c3, c4));
    }
    Figure *create(const std::vector<Coordinations> &v){
        return reinterpret_cast<Figure*>(new Rombus(v));
    }
};

class Pentagon_Factory: public Factory{
public:
    Figure *create(){
        return reinterpret_cast<Figure*>(new Pentagon());
    }
    Figure *create(Coordinations c, double radius, Coordinations c1){
        return reinterpret_cast<Figure*>(new Pentagon(c, radius, c1));
    }

    Figure *create(const Coordinations &c1, const Coordinations &c2, const Coordinations &c3, const Coordinations &c4, const Coordinations &c5){
        return reinterpret_cast<Figure*>(new Pentagon(c1, c2, c3, c4, c5));
    }
    Figure *create(const std::vector<Coordinations> &v){
        return reinterpret_cast<Figure*>(new Pentagon(v));
    }
};

class Hexagon_Factory: public Factory{
public:
    Figure *create(){
        return reinterpret_cast<Figure*>(new Hexagon());
    }
    Figure *create(Coordinations c, double radius, Coordinations c1){
        return reinterpret_cast<Figure*>(new Hexagon(c, radius, c1));
    }
    Figure *create(const Coordinations &c1, const Coordinations &c2, const Coordinations &c3, const Coordinations &c4, const Coordinations &c5, const Coordinations &c6){
        return reinterpret_cast<Figure*>(new Hexagon(c1, c2, c3, c4, c5, c6));
    }
    Figure *create(const std::vector<Coordinations> &v){
        return reinterpret_cast<Figure*>(new Hexagon(v));
    }
};

#endif