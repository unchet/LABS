#include <iostream>
#include <vector>
#include <memory>
#include <string>

#include "figures.hpp"
#include "file_vector.hpp"

void menu(){
	std::cout << "\nMenu:\n";
	std::cout << "1. Push\n";
	std::cout << "2. Pop\n";
	std::cout << "3. Undo\n";
	std::cout << "4. Import\n";
	std::cout << "5. Export\n";
	std::cout << "6. Print\n";
	std::cout << "7. Print menu\n";
	std::cout << "0. Exit" << std::endl;
}

void push_menu(){
	std::cout << "\n1. Push front\n";
	std::cout << "2. Push back\n";
}

void pop_menu(){
	std::cout << "\n1. Pop front\n";
	std::cout << "2. Pop back\n";
}

int main(){
	std::unique_ptr<Rombus_Factory> r(new Rombus_Factory);
	std::unique_ptr<Pentagon_Factory> p(new Pentagon_Factory);
	std::unique_ptr<Hexagon_Factory> h(new Hexagon_Factory);

	Vector sv;
	menu();
	int figure;
	int choice;
	Coordinations c1, c2, c3, c4;
	double radius;
	while(1){
		std::cout << "Enter the number: ";
		std::cin >> choice;
		
		std::string figure_name;
		std::string file_name;

		switch(choice){
			case 1:{
				push_menu();
				std::cin >> choice;
				std::cout << "Choose the figure:\n";
				std::cout << "1. Rhombus\n";
				std::cout << "2. Pentagon\n";
				std::cout << "3. Hexagon\n";
				std::cin >> figure;
				switch(choice){
					case 1:{
						switch(figure){
							case 1:{
								std::cout << "Enter coordinates: ";
								std::cin >> c1 >> c2 >> c3 >> c4;
								if (c1 != c2 && c1 != c3 && c1 != c4 &&
									c2 != c3 && c2 != c4 && c3 != c4 && check(c1,c2,c3,c4)){
									sv.push_begin(r->create(c1, c2, c3, c4));
									std::cout << "Ready!" << std::endl;
								}
								else{
									std::cout << "Wrong coordinates" << std::endl;
								}
								break;
							}
							case 2:{
								std::cout << "Enter center and radius: ";
								std::cin >> c1;
								std::cin >> radius;
								std::cout << "Enter one point: ";
								std::cin >> c2;
								sv.push_begin(p->create(c1, radius, c2));
								std::cout << "Ready!" << std::endl;
								break;
							}
							case 3:{
								std::cout << "Enter center and radius: ";
								std::cin >> c1;
								std::cin >> radius;
								std::cout << "Enter one point: ";
								std::cin >> c2;
								sv.push_begin(h->create(c1, radius, c2));
								std::cout << "Ready!" << std::endl;
								break;
							}
						}
						break;
					}
					case 2:{
						switch(figure){
							case 1:{
								std::cout << "Enter coordinates: ";
								std::cin >> c1 >> c2 >> c3 >> c4;
								if (c1 != c2 && c1 != c3 && c1 != c4 &&
									c2 != c3 && c2 != c4 && c3 != c4){
									sv.push_end(r->create(c1, c2, c3, c4));
									std::cout << "Ready!" << std::endl;
								}
								else{
									std::cout << "Wrong coordinates" << std::endl;
								}
								break;
							}
							case 2:{
								std::cout << "Enter center and radius: ";
								std::cin >> c1;
								std::cin >> radius;
								std::cout << "Enter one point: ";
								std::cin >> c2;
								sv.push_end(p->create(c1, radius, c2));
								std::cout << "Ready!" << std::endl;
							}
							case 3:{
								std::cout << "Enter center and radius: ";
								std::cin >> c1;
								std::cin >> radius;
								std::cout << "Enter one point: ";
								std::cin >> c2;
								sv.push_end(p->create(c1, radius, c2));
								std::cout << "Ready!" << std::endl;
							}
						}
						break;
					}
					default:
						std::cout << "Wrong number" << std::endl;
				}
				break;
			}
			case 2:{
				pop_menu();
				std::cin >> choice;
				switch(choice){
					case 1:
						if(!sv.pop_begin()){
							std::cout << "There is no figures" << std::endl;
						}
						else{
							std::cout << "Ready!" << std::endl;
						}
						break;
					case 2:
						if(!sv.pop_end()){
							std::cout << "There is no figures" << std::endl;
						}
						else{
							std::cout << "Ready!" << std::endl;
						}
						break;
					default:
						std::cout << "Wrong number" << std::endl;
				}
				break;
			}
			case 3:{
				if(sv.undo()){
					std::cout << "Ready!" << std::endl;
				}

				break;
			}
			case 4:{
				std::cout << "Enter filename" << std::endl;
				std::cin >> file_name;
				if(sv.import_file(file_name)){
					std::cout << "Ready!" << std::endl;
				}
				else{
					std::cout << "Something went wrong" << std::endl;
				}
				break;
			}
			case 5:{
				std::cout << "Enter filename" << std::endl;
				std::cin >> file_name;
				if(sv.export_file(file_name)){
					std::cout << "Ready!" << std::endl;
				}
				else{
					std::cout << "Something went wrong" << std::endl;
				}
				break;  
			}
			case 6:{
				if(!sv.print())
					std::cout << "There is no figures" << std::endl;
				break;
			}
			case 7:{
				menu();
				break;
			}
			case 0:{
				return 0;
			}
			default:
				std::cout << "Wrong number" << std::endl;
		}
	}
	return 0;
}