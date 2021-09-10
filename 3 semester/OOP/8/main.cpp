#include <iostream>
#include <memory>
#include <vector>
#include <thread>
#include <mutex>
#include <condition_variable>

#include "figures.hpp"
#include "event.hpp"

void handle(std::vector<std::unique_ptr<Figure>>& figures, int buf_size, std::condition_variable &main_thread, 
			std::condition_variable &handle_thread, std::mutex &mutex, bool &stop){


	std::unique_lock<std::mutex> lock(mutex);
	handle_thread.notify_all();
	std::vector<std::unique_ptr<Handler>> handlers;

	handlers.push_back(std::make_unique<File_Handler>());
	handlers.push_back(std::make_unique<Console_Handler>());

	while(1){
		main_thread.wait(lock);
		if(stop)
			break;
		
		for(int i = 0; i < handlers.size(); ++i){
			handlers[i]->execute(figures);
		}
		figures.clear();
		handle_thread.notify_all();
	}
	return;
}

int main(int argc, char** argv){
	if(argc != 2){
		std::cout << "Usage: " << argv[0] << " <buffer_size>" << std::endl;
		return 1;
	}

	std::condition_variable main_thread;
	std::condition_variable handle_thread;
	std::vector<std::unique_ptr<Figure>> figures;
	std::unique_ptr<TriangleFactory> t(new TriangleFactory);
	std::unique_ptr<SquareFactory> s(new SquareFactory);
	std::unique_ptr<RectangleFactory> r(new RectangleFactory);
	std::mutex mutex;
	std::unique_lock<std::mutex> lock(mutex);
	int buf_size, check_buf = 0, action;
	char answer;
	buf_size = std::stoi(argv[1]);
	bool stop = false;
	std::thread handler(handle, std::ref(figures), buf_size, std::ref(main_thread), std::ref(handle_thread), std::ref(mutex), std::ref(stop));
	handle_thread.wait(lock);

	while(1){
			for(int i = 0; i < buf_size; ++i){
			std::cout << "1. Push triangle\n"; 
			std::cout << "2. Push square\n"; 
			std::cout << "3. Push rectangle\n";
			std::cout << "0. Exit" << std::endl;
			std::cin >> action;
			switch(action){
				case 1:{
					std::cout << "Enter coordinates: ";
					auto tf = t->create(std::cin);
					if(tf == nullptr){
						std::cout << "Wrong coordinates" << std::endl;
						--i;
					}else{
						figures.push_back(t->create(std::move(tf)));
						std::cout << "Ready!" << std::endl;
					}

					break;
				}
				case 2:{
					std::cout << "Enter coordinates: ";
					auto sf = s->create(std::cin);
					if(sf == nullptr){
						std::cout << "Wrong coordinates" << std::endl;
						--i;
					}else{
						figures.push_back(s->create(std::move(sf)));
						std::cout << "Ready!" << std::endl;
					}

					break;
				}
				case 3:{
					std::cout << "Enter coordinates: ";
					auto rf = r->create(std::cin);
					if(rf == nullptr){
						std::cout << "Wrong coordinates" << std::endl;
						--i;
					}else{
						figures.push_back(r->create(std::move(rf)));
						std::cout << "Ready!" << std::endl;
					}

					break;
				}
				case 0:{
					std::cout << "Buffer is not full. Do you want to exit? (y/n)" << std::endl;
					std::cin >> answer;
					if(answer == 'y'){
						i = buf_size;
					}
					break;
				}
				default:{
					std::cout << "Wrong number" << std::endl;
					--i;
				}
			}
		}
		main_thread.notify_all();
		handle_thread.wait(lock);
		std::cout << "Continue? (y/n)" << std::endl;
		std::cin >> answer;
		if (answer != 'y')
			break;
	}

	stop = true;
	main_thread.notify_all();
	lock.unlock();
	handler.join();
	return 0;
}