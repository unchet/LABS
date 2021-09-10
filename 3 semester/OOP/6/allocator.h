#ifndef __ALLOCATOR__
#define __ALLOCATOR__

#include <iostream>
#include <cstdlib>
#include <stack>
#include <type_traits>

template <class T, size_t alloc_size>
struct allocator{
private:
	char *begin;
	char *end;
	char *tail;

	std::stack<char*> free_blocks;
public:
	template <class L>
	struct rebind{
		using other = allocator<L, alloc_size>;
	};

	allocator():
		begin(new char[alloc_size]),
		end(begin + alloc_size),
		tail(begin)
		{}

	allocator(const allocator&) = delete;
	allocator(allocator&) = delete;

	~allocator(){
		delete[] begin;
	}

	T* allocate(std::size_t n);
	void deallocate(T *ptr, std::size_t n);
};

template <class T, size_t alloc_size>
T *allocator<T, alloc_size>::allocate(std::size_t n){
	if(n != 1){
		throw std::logic_error("Can't allocate");
	}
	if(size_t(end - tail) < sizeof(T)){
		if(free_blocks.size()){
			char *ptr = free_blocks.top();
			free_blocks.pop();
			return reinterpret_cast<T*>(ptr);
		}
		throw::std::bad_alloc("Bad alloc");
	}
	T *res = reinterpret_cast<T*>(tail);
	tail += sizeof(T);
	return res;
}

template <class T, size_t alloc_size>
void allocator<T, alloc_size>::deallocate(T *ptr, std::size_t n){
	if(n != 1){
		throw std::logic_error("Can't deallocate");
	}
	if(ptr == nullptr){
		return;
	}
	free_blocks.push(reinterpret_cast<char*>(ptr));
}

#endif