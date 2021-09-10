CCFLAGS = -g3 -Wall -pedantic

CC = gcc

all: lib1.so lib2.so

lib1.so: realisation_1.c 
	$(CC) $(CCFLAGS) -c -fPIC realisation_1.c
	$(CC) $(CCFLAGS) -shared realisation_1.o -o lib1.so -lm

lib2.so: realisation_2.c
	$(CC) $(CCFLAGS) -c -fPIC realisation_2.c
	$(CC) $(CCFLAGS) -shared realisation_2.o -o lib2.so -lm

clean:
	rm *.o *.so