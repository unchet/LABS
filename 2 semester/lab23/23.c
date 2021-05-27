#include <stdio.h>
#include <stdlib.h>

typedef struct TreeNode TreeNode;

struct TreeNode {
    float value;
    TreeNode *father, *child, *sibling, *left_sibling;
};

TreeNode* makeNode(float val){
    TreeNode* node = (TreeNode*)malloc(sizeof(TreeNode));
    node->value = val;
    node->child = node->sibling = node->left_sibling = node->father =  NULL;
    return node;
}

void add(TreeNode* parent, TreeNode* newElement) {
    if (parent->child == NULL) {
        parent->child = newElement;
		newElement->father = parent;
        return;
    }
    TreeNode* current = parent->child;
    while (current->sibling != NULL) {
        current = current->sibling;
    }
    current->sibling = newElement;
	newElement->left_sibling = current;
}

void print(TreeNode* current, int d) {
    printf("%*s%.2f\n", 4 * d, " ", current->value);
    if (current->child != NULL) {
        print(current->child, d + 1);
    }
    if (current->sibling != NULL) {
        print(current->sibling, d);
    }
}

TreeNode* find(TreeNode* current, float value) {
    if (current == NULL)
        return current;
    
    if (value == current->value) 
        return current;
    
    TreeNode* tmp = find((current->child), value);
    if (tmp == NULL) 
        tmp = find((current->sibling), value);
    
    return tmp;
}

void clearTree(TreeNode* current){
	if(current->sibling != NULL)
		clearTree(current->sibling);
	
	if(current->child != NULL)
		clearTree(current->child);
	
	//После этого два варианта: или узел без братьев, или он самый "правый" брат
	if(current->left_sibling != NULL)
		current->left_sibling->sibling = NULL;
	else 
	current->father->child = NULL;

	free(current);	
}

void clearNode(TreeNode* need_to_delete) {
	//Если есть дети, то удаляем всё поддерево
	if(need_to_delete->child != NULL)
		clearTree(need_to_delete->child);
	
	//Если нет "левых" и "правых" братьев, то отцепляем узел от отца 
	if(need_to_delete->sibling == NULL && need_to_delete->left_sibling == NULL){
		//Если нет отца, то значит удаляемый узел - корень
		if(need_to_delete->father == NULL){
			need_to_delete = NULL;
		} else {
			need_to_delete->father->child = NULL;
		}
	//Если есть только "левые" братья, то отцепляем узел от левого брата
	} else if (need_to_delete->sibling == NULL && need_to_delete->left_sibling != NULL){
		(need_to_delete->left_sibling)->sibling = NULL;
	//Если есть только "правые" братья, то прикрепляем "правый" узел к отцу
	} else if (need_to_delete->sibling != NULL && need_to_delete->left_sibling == NULL){
		need_to_delete->father->child = need_to_delete->sibling;
		need_to_delete->sibling->father = need_to_delete->father;
		need_to_delete->sibling->left_sibling = NULL;
	//Если есть и "правые", и "левые" братья, то прикрепляем "левого" к "правому"
	} else {
		need_to_delete->left_sibling->sibling = need_to_delete->sibling;
		need_to_delete->sibling->left_sibling = need_to_delete->left_sibling;
		
	}
	free(need_to_delete);
}

//Поиск степени дерева
int NodeDegree(TreeNode* current, int number, int max_number){
	if(current->sibling != NULL){
		number++;
		max_number = NodeDegree(current->sibling, number, max_number);
	}
	if(number >= max_number)
		max_number = number;
	
	if(current->child != NULL){
		number = 1;
		max_number = NodeDegree(current->child, number, max_number);
	}
	return max_number;
}

int main(){
	
	TreeNode* root = NULL;    
    float val, ques, del;
	int number = 0, max_number = 0, user_choice=1;
	char c = ' ';
	
	printf("Приветствую Вас в моей программе\n");
	
	while(user_choice){
		
		printf("\n\tВыберите действие в меню"
			   "\n\t===================================="
			   "\n\t||              Меню              ||"
               "\n\t||--------------------------------||"
               "\n\t|| 0 - Выход из программы         ||"
               "\n\t|| 1 - Добавить узлы              ||"
               "\n\t|| 2 - Вывести дерево на экран    ||"
               "\n\t|| 3 - Удалить узел               ||"
               "\n\t|| 4 - Удалить дерево             ||"
		       "\n\t|| 5 - Найти степень дерева       ||"
               "\n\t===================================="
               "\n\n ==> ");
	  
		if(scanf("%d",&user_choice)){
	
			switch(user_choice){
				case 0:
					printf("Программа завершена\n");
					break;
				case 1:
					if(root == NULL){
						printf("Введите корень дерева\n ==> ");
						scanf("%f", &val);
						root = makeNode(val);
						break;
					}
					if(root->child == NULL){
						printf("Какие узлы присоединить к корню?\n ==> ");
						ques = root->value;
					}
					else {
						printf("К какому узлу присоединять?\n ==> ");
						scanf("%f", &ques);
						while(find(root,ques) == NULL){
							printf("Такого узла нет, выберите другой\n");
							printf("К какому узлу присоединять?\n ==> ");
							scanf("%f", &ques);
						}
						printf("Какие узлы присоединить?\n ==> ");
					}
					c = ' ';
					while (c != '\n' && scanf("%f", &val) == 1) {
						add(find(root,ques), makeNode(val));
						c = getchar();
					}
					break;
						
				case 2:
					if(root != NULL)
						print(root,0);
					else 
						printf("Дерево не создано. Добавьте корень\n");
					
					break;
					
				case 3:
					if(root != NULL){
						printf("Какой узел удалить?\n ==> ");
						scanf("%f", &del);
						while(find(root,del) == NULL){
							printf("Такого узла нет, выберите другой\n");
							printf("Какой узел удалить?\n ==> ");
							scanf("%f", &del);
						}
						clearNode(find(root,del));
						if (root->value == del){
							free(root);
							root = NULL;
						}
						printf("Узел удалён\n");
					} else
						printf("Дерево не создано. Добавьте корень\n");
					break;
						
				case 4:
					if(root != NULL){
						clearNode(root);
						free(root);
						root = NULL;
						printf("Дерево удалено\n");
					} else
						printf("Дерево не создано. Добавьте корень\n");
					break;
					
				case 5:
					if(root != NULL){
						printf("Степень дерева равна %d\n", NodeDegree(root,number,max_number));
					} else
							printf("Дерево не создано. Добавьте корень\n");
						break;					
						
						default:
					printf("Выбран неверный номер из меню, повторите попытку\n");
			}
		
		} else {
			printf("Вы ввели не цифру. Программа завершена\n");
			break;
			}
	}

	if(root != NULL){
		clearNode(root);
		free(root);
	}
	
	return 0;
}





