all: lab26

lab26: lab26.o stack.o
	gcc -Wall lab26.o stack.o -o lab26

lab26.o: lab26.c
	gcc -c -Wall lab26.c

stack.o: stack.c
	gcc -c -Wall stack.c

clean:
	rm -f *.o