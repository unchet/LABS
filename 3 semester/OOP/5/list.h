#ifndef __LIST__
#define __LIST__

#include <memory>

template<class T>
	class list {
	private:
		struct node;
		int size = 0;
	public:
		list() = default;

		class forward_iterator {
		public:
			using value_type = T;
			using reference = value_type&;
			using pointer = value_type*;
			using difference_type = std::ptrdiff_t;
			using iterator_category = std::forward_iterator_tag;
			explicit forward_iterator(node *ptr);
			T& operator*();
			forward_iterator& operator++();
			forward_iterator operator++(int);
			bool operator== (const forward_iterator &other) const;
			bool operator!= (const forward_iterator &other) const;
		private: 
			node *it_ptr;
			friend list;
		};

		forward_iterator begin();
		forward_iterator end();
		void push_back(T& value);
		void push_front(T& value);
		T& front();
		T& back();
		void pop_back();
		void pop_front();
		int length();
		bool is_empty();
		void clear(forward_iterator it);
		void delete_by_idx(auto N);
		void insert(forward_iterator it, T &value);
		void insert_by_idx(auto N, T &value);
		list& operator=(list& other);
		T& operator[](auto index);

	private:
		struct node {
			T value;
			std::unique_ptr<node> next;
			node *prev = nullptr;
			node(const T& value_) : value(value_) {}
			forward_iterator next_it();
		};

		std::unique_ptr<node> first;
		node *last = nullptr;
	};

	template<class T>
	typename list<T>::forward_iterator list<T>::begin() {
		return forward_iterator(first.get());
	}

	template<class T>
	typename list<T>::forward_iterator list<T>::end() {
		return forward_iterator(nullptr);
	}

	template<class T>
	int list<T>::length() {
		return size;
	}

	template<class T>
	bool list<T>::is_empty() {
		return length() == 0;
	}

	template<class T>
	void list<T>::push_back(T& value) {
		if (!size) {
			first = std::make_unique<node>(value);
			last = first.get();
			size++;
			return;
		}
		last->next = std::make_unique<node>(value);
		node *tmp = last;
		last = last->next.get();
		last->prev = tmp;
		size++;
	}

	template<class T>
	void list<T>::push_front(T& value) {
		size++;
		std::unique_ptr<node> tmp = std::move(first);
		first = std::make_unique<node>(value);
		first->next = std::move(tmp);
		if (first->next != nullptr)
			first->next->prev = first.get();
		if (size == 1) {
			last = first.get();
		}
		if (size == 2) {
			last = first->next.get();
		}
	}

	template<class T>
	void list<T>::pop_front() {
		if (size == 0) {
			std::cout << "List is empty" << std::endl;
			return;
		}
		if (size == 1) {
			first = nullptr;
			last = nullptr;
			size--;
			return;
		}
		std::unique_ptr<node> tmp = std::move(first->next);
		first = std::move(tmp);
		first->prev = nullptr;
		size--;
	}

	template<class T>
	void list<T>::pop_back() {
		if (size == 0) {
			std::cout << "List is empty" << std::endl;
			return;
		}
		if (last->prev) {
			node *tmp = last->prev;
			last->prev->next = nullptr;
			last = tmp;
		}
		else {
			first = nullptr;
			last = nullptr;
		}
		size--;
	}


	template<class T>
	T& list<T>::front() {
		if (size == 0) {
			throw std::logic_error("List is empty");
		}
		return first->value;
	}

	template<class T>
	T& list<T>::back() {
		if (size == 0) {
			throw std::logic_error("List is empty");
		}
		forward_iterator i = this->begin();
		while (i.it_ptr->next_it() != this->end()) {
			i++;
		}
		return *i;
	}
	template<class T>
	list<T>& list<T>::operator=(list<T> &other) {
		size = other.size;
		first = std::move(other.first);
	}

	template<class T>
	void list<T>::clear(forward_iterator it) {
		if (it == this->end()) throw std::logic_error("Wrond idx");
		if (it == this->begin()) {
			this->pop_front();
			return;
		}
		if (it.it_ptr == last) {
			this->pop_back();
			return;
		}

		if (it.it_ptr == nullptr) throw std::logic_error("Wrond idx");
		auto tmp = it.it_ptr->prev;
		std::unique_ptr<node> tmp2 = std::move(it.it_ptr->next);
		it.it_ptr = it.it_ptr->prev;
		it.it_ptr->next = std::move(tmp2);
		it.it_ptr->next->prev = tmp;

		size--;
	}

	template<class T>
	void list<T>::delete_by_idx(auto N) {
		forward_iterator it = this->begin();
		for (size_t i = 0; i < N; ++i) {
			++it;
		}
		this->clear(it);
	}

	template<class T>
	void list<T>::insert(forward_iterator it, T &value) {
		std::unique_ptr<node> tmp = std::make_unique<node>(value);
		if (it == this->begin()) {
			this->push_front(value);
			return;
		}
		if (it.it_ptr == nullptr) {
			this->push_back(value);
			return;
		}
		
		tmp->prev = it.it_ptr->prev;
		it.it_ptr->prev = tmp.get();
		tmp->next = std::move(tmp->prev->next);
		tmp->prev->next = std::move(tmp);

		size++;
	}

	template<class T>
	void list<T>::insert_by_idx(auto N, T &value) {
		forward_iterator it = this->begin();
		if (N >= this->length())
			it = this->end();
		else
			for (auto i = 0; i < N; ++i) {
				++it;
			}
		this->insert(it, value);
	}
	template<class T>
	typename list<T>::forward_iterator list<T>::node::next_it() {
		return forward_iterator(this->next.get());
	}

	template<class T>
	list<T>::forward_iterator::forward_iterator(node *ptr) {
		it_ptr = ptr;
	}

	template<class T>
	T& list<T>::forward_iterator::operator*() {
		return this->it_ptr->value;
	}
	template<class T>
	T& list<T>::operator[](auto idx) {
		if (idx < 0 || idx >= size) {
			throw std::out_of_range("Wrong idx");
		}
		forward_iterator it = this->begin();
		for (size_t i = 0; i < idx; i++) {
			it++;
		}
		return *it;
	}

	template<class T>
	typename list<T>::forward_iterator& list<T>::forward_iterator::operator++() {
		*this = it_ptr->next_it();
		return *this;
	}

	template<class T>
	typename list<T>::forward_iterator list<T>::forward_iterator::operator++(int) {
		forward_iterator tmp = *this;
		++ *this;
		return tmp;
	}

	template<class T>
	bool list<T>::forward_iterator::operator==(const forward_iterator& other) const {
		return it_ptr == other.it_ptr;
	}

	template<class T>
	bool list<T>::forward_iterator::operator!=(const forward_iterator& other) const {
		return it_ptr != other.it_ptr;
	}

#endif