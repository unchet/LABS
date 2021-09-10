#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <signal.h>
#include <unistd.h>
#include <sys/prctl.h>

#define BUFF_SIZE 256

int read_A;
int read_C;

int main(int argc, char **argv) {
    pid_t parent_pid = atoi(argv[1]);
    if (getppid() != parent_pid) {
        exit(EXIT_FAILURE);
    }

    read_A = atoi(argv[2]);
    read_C = atoi(argv[3]);

    size_t from_A;
    size_t from_C;
    while (1) {
        read(read_A, &from_A, sizeof(size_t));
        read(read_C, &from_C, sizeof(size_t));
        printf("B got length %ld from A\n", from_A);
        printf("B got length %ld from C\n", from_C);
    }

    return 0;
}

