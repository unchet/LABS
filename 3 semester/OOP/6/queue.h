#ifndef __QUEUE__
#define __QUEUE__

#include <memory>
#include <unistd.h>
#include <exception>
#include "allocator.h"

template<class T, class Allocator = std::allocator<T>>
class queue {
private:
	struct element;
	int size = 0;
public:
	queue() = default;

	class forward_iterator {
	public:
		explicit forward_iterator(element* ptr);
		T& operator*();
		forward_iterator& operator++();
		forward_iterator operator++(int);
		bool operator== (const forward_iterator& other) const;
		bool operator!= (const forward_iterator& other) const;
	private:
		element* it_ptr;
		friend queue;
	};

	forward_iterator begin();
	forward_iterator end();
	void push(const T& value);
	T& top();
	void pop();
	void delete_by_number(size_t number);
	int length();
	bool empty();
	queue& operator=(queue& other);
private:
	using allocator_type = typename Allocator::template rebind<element>::other;
	struct deleter{
	private:
		allocator_type *allocator_;
	public:
		deleter(allocator_type *allocator) : allocator_(allocator) {}
		void operator()(element *ptr){
			if(ptr != nullptr){
				std::allocator_traits<allocator_type>::destroy(*allocator_, ptr);
				allocator_->deallocate(ptr,1);
			}
		}
	};
	using unique_ptr = std::unique_ptr<element, deleter>;
	struct element {
		T value;
		unique_ptr next = {nullptr, deleter{nullptr}};
		element *prev = nullptr;
		element(const T& value_) : value(value_) {}
		forward_iterator next_it();
	};

	allocator_type allocator_{};
	unique_ptr first{nullptr, deleter{nullptr}};
	element* tail = nullptr;
};

template<class T, class Allocator>
typename queue<T, Allocator>::forward_iterator queue<T, Allocator>::begin() {
	return forward_iterator(first.get());
}

template<class T, class Allocator>
typename queue<T, Allocator>::forward_iterator queue<T, Allocator>::end() {
	return forward_iterator(nullptr);
}
template<class T, class Allocator>
int queue<T, Allocator>::length() {
	return size;
}
template<class T, class Allocator>
bool queue<T, Allocator>::empty() {
	return length() == 0;
}

template<class T, class Allocator>
void queue<T, Allocator>::push(const T& value) {
	element *res = this->allocator_.allocate(1);
	std::allocator_traits<allocator_type>::construct(this->allocator_, res, value);
	if (!size) {
		first = unique_ptr(res, deleter{&this->allocator_});
		tail = first.get();
		size++;
		return;
	}
	tail->next = unique_ptr(res, deleter{&this->allocator_});
	element* temp = tail;
	tail = tail->next.get();
	tail->prev = temp;
	size++;
}

template<class T, class Allocator>
void queue<T, Allocator>::pop() {
	if (!size) {
		std::cout << "Queue is empty" << std::endl;
		return;
	}
	if (size == 1) {
		first = nullptr;
		tail = nullptr;
		size--;
		return;
	}
	unique_ptr tmp = std::move(first->next);
	first = std::move(tmp);
	first->prev = nullptr;
	size--;
}

template<class T, class Allocator>
void queue<T, Allocator>::delete_by_number(size_t number){
	if(!size){
		std::cout << "Queue is empty" << std::endl;
		return;
	}
	if(number >= size){
		std::cout << "Index is too big" << std::endl;
		return;
	}
	while(number > 0){
		T tmp = top();
		pop();
		push(tmp);
		number--;
	}
	pop();
}

template<class T, class Allocator>
T& queue<T, Allocator>::top() {
	if (!size) {
		throw std::logic_error("Queue is empty");
	}
	return first->value;
}

template<class T, class Allocator>
queue<T, Allocator>& queue<T, Allocator>::operator=(queue<T, Allocator> &other) {
	size = other.size;
	first = std::move(other.first);
}

template<class T, class Allocator>
typename queue<T, Allocator>::forward_iterator queue<T, Allocator>::element::next_it() {
	return forward_iterator(this->next.get());
}

template<class T, class Allocator>
queue<T, Allocator>::forward_iterator::forward_iterator(queue<T, Allocator>::element *ptr) {
	it_ptr = ptr;
}

template<class T, class Allocator>
T& queue<T, Allocator>::forward_iterator::operator*() {
	return this->it_ptr->value;
}

template<class T, class Allocator>
typename queue<T, Allocator>::forward_iterator& queue<T, Allocator>::forward_iterator::operator++() {
	if (it_ptr == nullptr) throw std::logic_error("out of queue borders");
	*this = it_ptr->next_it();
	return *this;
}

template<class T, class Allocator>
typename queue<T, Allocator>::forward_iterator queue<T, Allocator>::forward_iterator::operator++(int) {
	forward_iterator old = *this;
	++ *this;
	return old;
}

template<class T, class Allocator>
bool queue<T, Allocator>::forward_iterator::operator==(const forward_iterator& other) const {
	return it_ptr == other.it_ptr;
}

template<class T, class Allocator>
bool queue<T, Allocator>::forward_iterator::operator!=(const forward_iterator& other) const {
	return it_ptr != other.it_ptr;
}

#endif