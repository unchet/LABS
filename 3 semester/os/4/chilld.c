#include <fcntl.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <unistd.h>

#define MAX_SIZE 512

int is_vowel(char c){
	if (c=='a' || c=='A' || c=='e' || c=='E' || c=='i' || c=='I' ||
		c=='o' || c=='O' || c=='u' || c=='U' || c=='y' || c=='Y')
		return 1;
	return 0;
}

void del_vowel(char *str, char *res, int l){
	for(int i=0, k=0; i < l; ++i){
		if(is_vowel(str[i])){
			continue;
		}
		res[k] = str[i];
		++k;
	}
}

int main(int argc, char **argv){
	char str[MAX_SIZE];
	char *addr;

	int fd = open(argv[1], O_RDWR, S_IRWXU);
	if (fd == -1){
		perror("Error creating shared child file!\n");
		exit(errno);
	}

	struct stat st;
	if(fstat(fd, &st) < 0){
		perror("fstat error");
		exit(errno);
	}
	addr = mmap(NULL, st.st_size, PROT_WRITE | PROT_READ , MAP_SHARED, fd, 0);
	if (addr == MAP_FAILED){
		perror("mmap error");
		exit(errno);
	}

	strcpy(str, addr);	
	close(fd);
	remove(argv[1]);

	int l = strlen(str);
	char *res = (char*) malloc(sizeof(char) * l);
	del_vowel(str, res, l);
	write(1, res, strlen(res) + 1);
	free(res);
	return 0;
}