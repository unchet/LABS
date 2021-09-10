#include <iostream>
#include <algorithm>
#include "queue.h"
#include "allocator.h"
#include "rectangle.h"

int main() {
	queue<Rectangle<int>> q;

	Rectangle<int> tmp;

	while (true) {
		std::cout << "\tМеню" << std::endl;
		std::cout << "1. Добавить фигуру в очередь\n";
		std::cout << "2. Удалить фигуру\n";
		std::cout << "3. Вывести все фигуры\n";
		std::cout << "0. Выйти из программы\n";

		int n;
		double s;
		std::cin >> n;
		switch (n) {
		case 1:
			std::cout << "Введите координаты: " << std::endl;
			tmp.read(std::cin);
			if(!tmp.check()){
				std::cout << "Ошибка в координатах" << std::endl;
			} else{
				q.push(tmp);
			}
			break;
		case 2:
			std::cout << "1. Удалить фигуру в начале очереди\n";
			std::cout << "2. Удалить фигуру по индексу\n";
			std::cin >> n;
			switch (n) {
			case 1:
				q.pop();
				break;
			case 2:
				std::cout << "Введите индекс:" << std::endl;
				std::cin >> n;
				q.delete_by_number(n);
				break;
			default:
				break;
			}
			break;
		case 3:
			std::cout << "\nКоличество фигур: " << q.length() << std::endl << std::endl;
			std::for_each(q.begin(), q.end(), [](Rectangle<int>& X) { X.print(std::cout); std::cout << std::endl; });
			break;
		case 0:
			return 0;
		default:
			std::cout << "Неправильный номер" << std::endl;
		}
	}

	return 0;
}