#ifndef __EVENT__
#define __EVENT__

#include <string>
#include <memory>
#include <fstream>
#include "figures.hpp"

struct Handler {
	virtual void execute(std::vector<std::unique_ptr<Figure>>& figures ) = 0;
	virtual ~Handler() = default;
};

struct File_Handler : Handler {
	void execute(std::vector<std::unique_ptr<Figure>>& figures) override {
		std::string filename;

		std::cout << "Write filename\n";
		std::cin >> filename;
		
		std::ofstream file(filename);
		for (int i = 0; i < figures.size(); ++i) {
			figures[i]->Print(file);
		}
	}
};
struct Console_Handler : Handler {
	void execute(std::vector<std::unique_ptr<Figure>>& figures) override {
		for (int i = 0; i < figures.size(); ++i) {
			figures[i]->Print(std::cout);
		}
	}
};

#endif