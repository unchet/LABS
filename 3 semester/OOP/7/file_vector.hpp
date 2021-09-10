#ifndef __VECTOR__
#define __VECTOR__

#include <fstream>
#include <iostream>
#include <stack>
#include <vector>
#include <string>
#include <ctime>
#include <cstdlib>
#include <cmath>

#include "figures.hpp"

struct command_figure{
	char figure_type;
	std::string cmd;
	Figure *f;
};

class Vector{
private:
	Rombus_Factory *r;
	Pentagon_Factory *p;
	Hexagon_Factory *h;

	std::vector<Figure*> storage;
	std::fstream file;

	bool is_file_opened;
	bool is_buffer_saved;

	std::stack<command_figure> commands;

public:
	Vector(){
		srand(time(NULL));
		is_buffer_saved = true;
		is_file_opened = false;
		r = new Rombus_Factory;
		p = new Pentagon_Factory;
		h = new Hexagon_Factory;
	}
	~Vector(){
		if(file.is_open()){
			file.close();
		}
		
		clear_storage();
		clear_stack();
		delete r;
		delete p;
		delete h;
	}

	bool open_document(std::string s){
		bool is_file_exists = check_exist(s);
		while(is_file_exists){
			std::cout << "File with name \'"<< s << "\' already exists.\n" <<
			"If you will continue, data will be lost\n" << "Continue? (y/n): ";
			char choice;
			std::cin >> choice;
			if(choice != 'y'){
				return false;
			}
		}			
		std::ofstream ofs;
		ofs.open(s);

		if(ofs.is_open()){
			ofs.close();
			file.open(s, std::ios::in | std::ios::out | std::ios::binary);
			if(file.is_open()){
				is_file_opened = true;
				return true;
			}else{
				std::cout << "Error with opening file\n";
				return false;
			}
		}else{
			std::cout << "Error with opening file\n";
			return false;
		}
	}

	void push_begin(Figure *f){
		char type = f->get_figure();
		storage.insert(storage.begin(), f);
		commands.push({type, "pop_begin", nullptr});
		is_buffer_saved = false;
	}

	bool pop_begin(){
		if(!storage.empty()){
			Figure *f = storage.front();
			char type = f->get_figure();
			storage.erase(storage.begin());
			commands.push({type, "push_begin", f});
			is_buffer_saved = false;
			return true;
		}
		return false;
	}

	void push_end(Figure *f){
		char type = f->get_figure();
		storage.push_back(f);
		commands.push({type, "pop_end", nullptr});
		is_buffer_saved = false;
	}

	bool pop_end(){
		if(!storage.empty()){
			Figure *f = storage.back();
			char type = f->get_figure();
			storage.pop_back();
			commands.push({type, "push_end", f});
			is_buffer_saved = false;
			return true;
		}
		return false;
	}

	bool export_file(std::string s){

		bool is_file_exists = check_exist(s);
		if(is_file_exists){
			std::cout << "File with name \'"<< s << "\' already exists.\n" <<
			"If you will continue, data will be lost\n" << "Continue? (y/n): ";
			char choice;
			std::cin >> choice;
			if(choice != 'y'){
				return false;
			}
		}

		std::ofstream temp;
		temp.open(s);
		temp.close();

		std::fstream file_to_export;
		file_to_export.open(s, std::ios::out | std::ios::binary);

		if(!file_to_export.is_open()){
			std::cout << "Can not open file for export data\n";
			return false;
		}

		size_t storage_size = storage.size();
		file_to_export.write( (char*)&storage_size, sizeof(storage.size()) );
		for(size_t i = 0; i < storage_size; i++){
			
			char figure_type = storage[i]->get_figure();
			file_to_export.write((char*)&figure_type, sizeof(figure_type));

			for(size_t j = 0; j < storage[i]->cords.size(); j++){
				file_to_export.write( (char*)(&storage[i]->cords[j]), sizeof(Coordinations) );
			}
		}
		file_to_export.close();
		is_buffer_saved = true;
		return true;
	}

	bool import_file(std::string s){
		if(!is_buffer_saved){
			std::cout << "Buffer is not saved.\n" <<
			"If you will continue, data will be lost\n" << "Continue? (y/n): ";
			
			char ans;
			std::cin >> ans;
			if(ans != 'y'){
				return false;
			}
		}
		clear_storage();
		clear_stack();

		if(file.is_open()){
			file.close();
		}

		file.open(s, std::ios::in | std::ios::out | std::ios::binary);
		
		if(!file.is_open()){
			std::cout << "Error. Can not import file\n";
			is_file_opened = false;
			return false;
		}else{
			size_t figures_number;
			file.read((char*)&figures_number, sizeof(figures_number));
			for(size_t i = 0; i < figures_number; i++){
				char figure_type;
				file.read((char*)&figure_type, sizeof(figure_type));
				Coordinations figure_cords[6];
				for(size_t j = 0; j < 6; j++){
					file.read((char*)&figure_cords[j], sizeof(figure_cords[j]));
					if(figure_type == 'r' && j == 3)
						break;
					if(figure_type == 'p' && j == 4)
						break;
				}
				switch(figure_type){
					case 'r':{
						storage.push_back(r->create(figure_cords[0],figure_cords[1],figure_cords[2],figure_cords[3]));
						break;
					}
					case 'p':{
						storage.push_back(p->create(figure_cords[0],figure_cords[1],figure_cords[2],figure_cords[3],figure_cords[4]));
						break;
					}
					case 'h':{
						storage.push_back(h->create(figure_cords[0],figure_cords[1],figure_cords[2],figure_cords[3],figure_cords[4],figure_cords[5]));
						break;
					}
					default:
						std::cout << "Error while reading from import_file file: wrong figure class\n";
						std::cout << figure_type << std::endl;
						break;
				}
			}
			is_buffer_saved = true;
			file.close();
			is_file_opened = false;
			return true;
		}
	}

	bool undo(){
		if(commands.empty()){
			std::cout << "There is no operations to undo\n";
			return false;
		}else{
			char figure_type = commands.top().figure_type;
			std::string action = commands.top().cmd;

			if(action == "push_begin"){
				if(figure_type == 'r'){
					storage.insert(storage.begin(), r->create(commands.top().f->cords));
				}else if(figure_type == 'p'){
					storage.insert(storage.begin(), p->create(commands.top().f->cords));
				}else if(figure_type == 'h'){
					storage.insert(storage.begin(), h->create(commands.top().f->cords));
				}else{
					std::cout << "Wrong figure type\n";
					return false;
				}
				delete commands.top().f;
			}else if(action == "pop_begin"){
				if(!storage.empty()){
					delete storage.front();
					storage.erase(storage.begin());
				}
			}else if(action == "push_end"){
				if(figure_type == 'r'){
					storage.push_back(r->create(commands.top().f->cords));
				}else if(figure_type == 'p'){
					storage.push_back(p->create(commands.top().f->cords));
				}else if(figure_type == 'h'){
					storage.push_back(h->create(commands.top().f->cords));
				}else{
					std::cout << "Wrong figure type:\n";
					return false;
				}
				delete commands.top().f;
			}else if(action == "pop_end"){
				if(!storage.empty()){
					delete storage.back();
					storage.pop_back();
				}
			}else if(action == "clear"){
				clear_storage();				
			}else{
				std::cout << "Error with undo\n";
				return false;
			}
			commands.pop();
			is_buffer_saved = false;
			return true;
		}
	}

	bool check_exist(std::string str){
		std::fstream fs;
		fs.open(str);
		if(fs.is_open()){
			fs.close();
			return true;
		}else{
			return false;
		}
	}

	bool print(){
		if(!storage.size())
			return false;
		for(size_t i = 0; i < storage.size(); i++){
			storage[i]->print();
		}
		return true;
	}

	size_t size(){
		return storage.size();
	}

	void clear_storage(){
		while(!storage.empty()){
			delete storage.back();
			storage.pop_back();
		}
	}

	void clear_stack(){
		while(!commands.empty()){
			delete commands.top().f;
			commands.pop();
		}
	}

	bool is_saved(){
		return is_buffer_saved;
	}

};

#endif