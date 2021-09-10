#include <fcntl.h>
#include <semaphore.h>
#include <stdio.h>
#include <stdio_ext.h>
#include <stdlib.h>
#include <string.h>
#include <errno.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <unistd.h>

#define FILENAME_LIMIT 255
#define SHARED_MEMORY_SIZE 512

const char *SHM_NAME1 = "shared_file1";
const char *SHM_NAME2 = "shared_file2";

void child_work(int fd, const char *tmp_fd){
	int child = fork();
	if(child < 0){
		perror("Fork error");
		exit(errno);
	}
	else if(!child){
		dup2(fd, 1);
		close(fd);
		execl("chilld", "chilld", tmp_fd, NULL);
	}
}

void clear(char *str){
	for(int i = 0; ;++i){
		if(str[i] == '\n'){
			str[i] = '\0';
			break;
		}
		str[i] = '\0';
	}
}

int main(int argc, char **argv){
	char *addr1;
	char *addr2;

	char *name1 = malloc(sizeof(char) * (FILENAME_LIMIT + 1));
	char *name2 = malloc(sizeof(char) * (FILENAME_LIMIT + 1));

	printf("Input first filename:\n");
	scanf("%s",name1);
	printf("Input second filename:\n");
	scanf("%s",name2);

	int f1 = open(name1, O_CREAT|O_RDWR|O_TRUNC, S_IREAD|S_IWRITE);
	if(f1 == -1){
		perror("Error creating file!\n");
		exit(errno);
	}

	int f2 = open(name2, O_CREAT|O_RDWR|O_TRUNC, S_IREAD|S_IWRITE);
	if(f2 == -1){
		perror("Error creating file!\n");
		exit(errno);
	}

	int tmp_f1 = open(SHM_NAME1, O_CREAT|O_RDWR|O_TRUNC, S_IREAD|S_IWRITE);
	if (tmp_f1 == -1){
		perror("Error creating file!\n");
		exit(errno);
	}

	int tmp_f2 = open(SHM_NAME2, O_CREAT|O_RDWR|O_TRUNC, S_IREAD|S_IWRITE);
	if (tmp_f2 == -1){
		perror("Error creating file!\n");
		exit(errno);
	}

	int len = 0;
	int cap = 1;
	char *str = (char*) malloc(cap * sizeof(char));
    printf("Input strings:\n");
	char c = ' ';
	__fpurge(stdin);
	while (c != EOF) {
		c = getchar();
		str[(len)++] = c;
		if (len >= cap) {
		cap *= 2;
		str = (char*) realloc(str, cap * sizeof(char));
		}
	}
	str[len] = '\0';

	char *strtmp = (char*) malloc(len * sizeof(char));
	char *str1 = (char*) malloc(len * sizeof(char));
	char *str2 = (char*) malloc(len * sizeof(char));
	for(int i = 0; i < len; ++i){
		strtmp[i] = 0;
		str1[i] = 0;
		str2[i] = 0;
	}

	for(int k = 0, i = 0; str[i]!='\0'; ++i, ++k){

		strtmp[k] = str[i];
		if(str[i] == '\n'){
			if(strlen(strtmp) <= 10){
				strcat(str1, strtmp);
				clear(strtmp);
				k=-1;
			}else{
				strcat(str2, strtmp);
				clear(strtmp);
				k=-1;
			}
		}
	}

	write(tmp_f1, str1, strlen(str1)+1);
	write(tmp_f2, str2, strlen(str2)+1);

	child_work(f1, SHM_NAME1);
	child_work(f2, SHM_NAME2);

	close(f1);
	close(f2);

	free(str);
	free(strtmp);
	free(str1);
	free(str2);
	free(name1);
	free(name2);

	return 0;	
}
