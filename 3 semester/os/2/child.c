#include <string.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

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

int main(){
	char str[MAX_SIZE];
	read(0, str, MAX_SIZE);
	int l = strlen(str);
	char *res = (char*) malloc(sizeof(char) * l);
	del_vowel(str, res, l);
	write(1, res, strlen(res) + 1);
	free(res);
	return 0;
}