#include <stdio.h>
#include <string.h>
#include <stdio_ext.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <errno.h>
#include <sys/stat.h>

#define MAX_SIZE 50
#define FILENAME_LIMIT 255

void clear(char *str){
	for(int i = 0; ;++i){
		if(str[i] == '\n'){
			str[i] = '\0';
			break;
		}
		str[i] = '\0';
	}
}

int main(){
	int pipe1[2], pipe2[2], f1, f2;
	if(pipe(pipe1)<0 || pipe(pipe2)<0){
		perror("Pipe error");
		exit(errno);
	}

	char *name1 = malloc(sizeof(char) * (FILENAME_LIMIT + 1));
	char *name2 = malloc(sizeof(char) * (FILENAME_LIMIT + 1));

	printf("Input first filename:\n");
	scanf("%s",name1);
	printf("Input second filename:\n");
	scanf("%s",name2);

	f1 = open(name1, O_CREAT|O_RDWR|O_TRUNC, S_IREAD|S_IWRITE);
	if(f1 == -1){
		perror("Error creating file!\n");
		exit(errno);
	}

	f2 = open(name2, O_CREAT|O_RDWR|O_TRUNC, S_IREAD|S_IWRITE);
	if(f2 == -1){
		perror("Error creating file!\n");
		exit(errno);
	}

	free(name1);
	free(name2);
	
	int child1 = fork(), child2;

	if (child1 < 0){
		perror("Fork error");
		exit(1);
	}else if(child1 >= 0){
		child2 = fork();
		if(child2 < 0){
			perror("Fork error");
			exit(errno);
		}
		else if (child1 > 0 && child2 > 0){ 
			printf("It's a parent, child1 id: [%d], child2 id: [%d]\n",child1,child2);
			int len = 0;
			int cap = 1;
			char *str = (char*) malloc(cap * sizeof(char));
			printf("Input strings:\n");
			__fpurge(stdin);
			char c = ' ';
			while (c != EOF) {
				c = getchar();
				str[(len)++] = c;
				if (len >= cap) {
				cap *= 2;
				str = (char*) realloc(str, cap * sizeof(char));
				}
			}
			str[len] = '\0';
			close(pipe1[0]);
			close(pipe2[0]);

			char *strtmp = (char*) malloc(len * sizeof(char));
			char *str1 = (char*) malloc(len * sizeof(char));
			char *str2 = (char*) malloc(len * sizeof(char));

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
			write(pipe1[1], str1, strlen(str1) + 1);
			write(pipe2[1], str2, strlen(str2) + 1);
			free(str);
			free(strtmp);
			free(str1);
			free(str2);
			close(pipe1[1]);
			close(pipe2[1]);
		} else if(!child1 && child2){
			dup2(pipe1[0],0);
			dup2(f1, 1);
			close(f1);
			close(f2);
			close(pipe1[0]);
			close(pipe1[1]);
			execl("child", "child", NULL);
		} else if(child1 && !child2){
			dup2(pipe2[0],0);
			dup2(f2, 1);
			close(f1);
			close(f2);
			close(pipe2[0]);
			close(pipe2[1]);
			execl("child", "child", NULL);
		}
	}
	return 0;
}