#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

typedef struct _ListEl ListEl;

struct _ListEl {
	double value;
	ListEl *next;
};

typedef struct {
	ListEl *head, *barrier;
	int sz;
} List;

typedef struct {
	ListEl *content;
} ListIterator;

ListIterator listBegin(List *l) {
	ListIterator it;
	it.content = l->head;
	return it;
}

ListIterator listEnd(List *l) {
	ListIterator it;
	it.content = l->barrier;
	return it;
}

bool equal(ListIterator a, ListIterator b) {
	return a.content == b.content;
}

bool next(ListIterator *it) {
	// ну или возвращать копию которая указывает на следующий элемент, не меняя текущий итератор
	if (it->content == NULL) {
		return false;
	}
	it->content = it->content->next;
	return true;
}

ListEl* makeElem(double value) {
	ListEl *newEl = malloc(sizeof(*newEl));
	newEl->value = value;
	return newEl;
}

int get_size(List *l){
	return l->sz;
}

List* initList() {
	List *tmp = malloc(sizeof(*tmp));
	ListEl *bar = malloc(sizeof(*bar));
	bar->value = -1;
	tmp->head = bar;
	tmp->barrier = bar;
	tmp->sz = 0;
	return tmp;
}

bool addFront(List *l, ListEl *newEl) {
	newEl->next =l->head;
	l->head = newEl;
	l->sz++;
	return true;
}

bool add(List *l, ListIterator it, ListEl *newEl) {
	if (equal(it, listEnd(l))) {
			return false;
	}
	newEl->next = it.content->next;
	it.content->next = newEl;
	l->sz++;
	return true;
}

void printList(List *l, ListIterator cur) {
	if (l->sz == 0) {
		printf("Empty list\n");
		return;
	}
	ListIterator it = listBegin(l);
	ListIterator end = listEnd(l);
	while (!equal(it, end)) {
		printf("%s%lf%s -> ", equal(it, cur)?"(":"", it.content->value, equal(it, cur)?")":"");
		next(&it);
	}
	printf("\n");
}

ListIterator getPointer(List *l, int n) {
	if (n < 0 || l->sz <= n) {
		return listEnd(l);
	}
	ListIterator it = listBegin(l);
	while (n) {
		next(&it);
		n--;
	}
	return it;
}



bool delete(ListIterator *it) {
	if (it->content == NULL) {
		return false;
	}
	ListEl *tmp = it->content->next;
	free(it->content);
	it->content = tmp;
	return true;
}

bool deleteFromList(List *l, ListIterator it) {
	// удаляет элемент следующий после указанного
	ListIterator tmp = it;
	next(&tmp);
	if (equal(tmp, listEnd(l))) {
		return false;
	}
	it.content->next = tmp.content->next;
	delete(&tmp);
	l->sz--;
	return true;
}

bool deleteHead(List *l) {
	if (l->sz == 0) {
		return false;
	}
	ListEl *tmp = l->head;
	l->head = tmp->next;
	free(tmp);
	l->sz--;
	return true;
}

bool deleteByIndex(List *l, int position) {
	bool success;
	if (position == 0) {
		success = deleteHead(l);
	} else {
		ListIterator it = getPointer(l, position - 1);
		if (equal(it, listEnd(l))) {
			success = false;
		} else {
			success = deleteFromList(l, it);
		}
	}
	return success;
}

bool addByIndex(List *l, int position, double value) {
	bool success;
	if (position == 0) {
		success = addFront(l, makeElem(value));
	} else {
		ListIterator it = getPointer(l, position - 1);
		if (equal(it, listEnd(l))) {
			success = false;
		} else {
			success = add(l, it, makeElem(value));
		}
	}
	return success;
}

void clearList(List *l) {
	ListIterator it = listBegin(l);
	ListIterator end = listEnd(l);
	while (!equal(it, end)) {
		delete(&it);
	}
	delete(&it);
	l->head = NULL;
	l->barrier = NULL;
	l->sz = 0;
}

int find_elem(List *l, ListIterator *it, int num){
	for(int i = 0; i < l->sz; i++){
		if(it->content->value == num)
			return i;
		it->content = it->content->next;
	}
	return -1;
}

int main() {
	List *l;
	l = initList();
	int action, k, a;
	int position;
	double value, value2;
	ListIterator current;
	printf("Выберите действие:\n"
		   "1. Добавить элемент по индексу\n"
		   "2. Удалить элемент по индексу\n"
		   "3. Добавить элемент после указанного\n"
		   "4. Удалить элемент по значению\n"
	       "5. Распечатка списка\n"
		   "6. Количество элементов в списке\n"
	       "7. Переместить итератор на указанный индекс\n"
	       "8. Переместить итератор на указанное число\n"
	       "9. Удалить k последних элементов\n"
		   "10. Поиск элемента\n");
	while (scanf("%d", &action) == 1) {
		switch (action) {
			case 1:
				printf("Введите индекс и значение:\n");
				scanf("%d %lf", &position, &value);
				if (addByIndex(l, position, value)) {
					printf("Элемент добавлен\n");
				} else {
					printf("Error\n");
				}
				break;
			case 2:
				printf("Введите индекс:\n");
				scanf("%d", &position);
				if (deleteByIndex(l, position)) {
					printf("Элемент удалён\n\n");
				} else {
					printf("Error\n");
				}
				break;
			case 3:
				printf("Введите число, после которого следует добавить элемент и само добавляемое число:\n");
				scanf("%lf %lf",&value, &value2);
				current = listBegin(l);
				a = find_elem(l, &current, value);
				if(a != -1){
					if(addByIndex(l,a + 1,value2))
						printf("Элемент добавлен\n");
				}
				else 
					printf("Error\n");
				break;
			case 4:
				printf("Какое число хотите удалить?\n");
				scanf("%lf", &value);
				current = listBegin(l);
				a = find_elem(l, &current, value);
				if(a != -1){
					if(deleteByIndex(l,a))
						printf("OK\n");
				} else
					printf("Error\n");
				break;
			case 5:
				printf("\n");
				current = listBegin(l);
				printList(l, current);
				printf("\n");
				break;
			case 6:
				printf("Количество элементов в списке: %d\n",get_size(l));
				break;
			case 7:
				printf("На какой индекс сместить итератор?\n");
				scanf("%d",&position);
				current = getPointer(l, position);
				printList(l, current);
				break;
			case 8:	
				printf("На какое число сместить итератор?\n");
				scanf("%lf",&value);
				current = listBegin(l);
				a  = find_elem(l, &current, value);
				current = getPointer(l, a);
				printList(l, current);
				break;
			case 9:
				printf("Сколько элементов удалить, начиная с конца?\n");
				scanf("%d",&k);
				for(; k > 0; k--){
					if(!deleteByIndex(l, l->sz - k))
						break;
				}
				if(k)
					printf("Error!!!\n");
				else
					printf("OK\n");
				break;
			case 10:
				printf("Введите число, которое хотите найти:\n");
				scanf("%lf",&value);
				current = listBegin(l);
				if(find_elem(l, &current, value) != -1)
					printf("Элемент %lf найден\n", current.content->value);
				else
					printf("Такого элемента в списке нет\n");
				break;
			case 0:
				clearList(l);
				free(l);
				return 0;
				
			default:
				printf("Wrong number\n");
		}
		printf("\nВыберите действие:\n"
		       "1. Добавить элемент по индексу\n"
			   "2. Удалить элемент по индексу\n"
			   "3. Добавить элемент после указанного\n"
			   "4. Удалить элемент по значению\n"
			   "5. Распечатка списка\n"
			   "6. Количество элементов в списке\n"
			   "7. Переместить итератор на указанный индекс\n"
			   "8. Переместить итератор на указанное число\n"
			   "9. Удалить k последних элементов\n"
			   "10. Поиск элемента\n"
			   "0. Выход из программы\n\n");
	}

	clearList(l);
	free(l);
	return 0;
}
