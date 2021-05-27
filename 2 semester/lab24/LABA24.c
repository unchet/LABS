#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#define N 20

typedef enum {
    NUMBER,
    VARIABLE,
    OPERATION,
    LBR,
    RBR,
    NONE
} TOKEN_TYPE;

typedef enum {
    PLUS = '+',
    MINUS = '-',
    MULT = '*',
    DIVIDE = '/',
    POWER = '^',
    UN_MINUS = '~'
} OPERATION_TYPE;

typedef struct {
    TOKEN_TYPE type;
    union {
        double number;
        char name[N];
        OPERATION_TYPE operation;
    } content;
} Token;

typedef struct Node {
	Token data;
	struct Node *next;
}StackElement;

typedef struct {
	StackElement *head;
}Stack;

Stack* initStack(){
	Stack *tmp = malloc(sizeof(*tmp));
	tmp->head = NULL;
	return tmp;
}

void push(Stack *s, Token data){
	StackElement *cur = malloc(sizeof(*cur));
	cur->next = s->head;
	s->head = cur;
	cur->data = data;
}

Token pop(Stack *s){
	StackElement *out;
	Token value;
	if(s->head == NULL)
		exit(-101);
	
	out = s->head;
	s->head = out->next;
	value = out->data;
	free(out);
	return value;
}

bool isStackEmpty(Stack *s){
	if (s->head == NULL)
		return true;
	return false;
}

void printStack(Stack *s){
	if(s->head == NULL)
		return;
	
	StackElement *head = s->head;
	
	while(head!=NULL){
		switch (head->data.type) {
			case NUMBER:
				printf("%lf\n", head->data.content.number);
				break;
			case VARIABLE:
				printf("%s\n", head->data.content.name);
				break;
			case OPERATION:
				printf("%c\n", head->data.content.operation);
				break;
			default:
				printf("Ошибка при вводе!\n");
			}
		head = head->next;
	}
	printf("\n");
}

void printReversePolish(Stack *s){
	if(s->head == NULL)
		return;
	StackElement *head = s->head;
	
	if(head != NULL){
		s->head = head->next;
		printReversePolish(s);
		switch (head->data.type) {
			case NUMBER:
				printf("%lf ", head->data.content.number);
				break;
			case VARIABLE:
				printf("%s ", head->data.content.name);
				break;
			case OPERATION:
				printf("%c ", head->data.content.operation);
				break;
			default:
				printf("Ошибка при вводе!\n");
		}
		s->head = head;
	}
}

void deleteStack(Stack *s){
	while(s->head != NULL)
		pop(s);
}


char _getNextSymbol() {
    // Пропускаем пробельные символы. Вспомогательная функция
    char c;
    do {
        c = getchar();
    } while (c == ' ' || c == '\t');
    return c;
} 

Token getToken(Token res, TOKEN_TYPE prevType) {
    char c = _getNextSymbol();
    if (c == '\n' || c == EOF) {
		res.content.name[0] = '\n';
    }
    if ((c >= '0' && c <= '9') || c == '.') {
        ungetc(c, stdin);
        scanf("%lf", &res.content.number);
        res.type = NUMBER;
    } else if ((c >= 'a' && c <= 'z') || (c >= 'A' && c <= 'Z') || c == '_') {
        ungetc(c, stdin);
        scanf("%[a-zA-Z_0-9]", res.content.name);
        res.type = VARIABLE;
    } else if (c == '(') {
        res.type = LBR;
    } else if (c == ')') {
        res.type = RBR;
    } else if (c == '-' || c == '~') {
        res.type = OPERATION;
		if(prevType == OPERATION || prevType == LBR || prevType == NONE)
			res.content.operation = UN_MINUS;
		else 		
			res.content.operation = c;
    } else if (c == '+' || c == '*' || c == '/' || c == '^'){
        res.type = OPERATION;
        res.content.operation = c;
    } else {
        res.type = NONE;
    }
    return res;
}

bool forcePush(OPERATION_TYPE a, OPERATION_TYPE b) { 
    // Проверяем нужно ли переместить операцию типа "a" в стек с результатом, если сейчас получили "b"
    switch (b) {
        case UN_MINUS:
            break;
        case POWER:
            if (a == UN_MINUS){
                return true;
            }
            break;
        case MULT: 
			if (a == UN_MINUS || a == POWER || a == MULT || a == DIVIDE){
				return true;
			}
			break;
        case DIVIDE:
            if (a == UN_MINUS || a == POWER || a == MULT || a == DIVIDE){
                return true;
            }
            break;
        case PLUS:
			if (a == UN_MINUS || a == POWER || a == MULT || a == DIVIDE || a == PLUS || a == MINUS){
                return true;
            }
			break;
        case MINUS:
			if (a == UN_MINUS || a == POWER || a == MULT || a == DIVIDE || a == PLUS || a == MINUS){
                return true;
            }
            break;
    }
    return false;
}


Stack* readAndConvertExpression(Stack *result) {
    // Считываем выражение и преобразуем его в постфиксную запись
    Stack *tmp;
	tmp = initStack();
    Token curToken;
    Token prevToken;
	prevToken.type = NONE;
	int check_un_minus = 0;

	bool okExpression = true;
    while (okExpression) {
		curToken = getToken(curToken, prevToken.type);
        if (curToken.type == NONE) {
			if (curToken.content.name[0] == '\n'){
				break;
			}
			okExpression = false;
			break;
        }
		
		Token check = prevToken;
        prevToken = curToken;
        Token topToken;
        switch (curToken.type) {
            case NUMBER:
				if(check.type == NUMBER || check.type == VARIABLE){
					okExpression = false;
					break;
				}
				if(check.type == OPERATION)
					if(check.content.operation == UN_MINUS)
						check_un_minus = 0;
				push(result, curToken);
				break;
            case VARIABLE:
				if(check.type == NUMBER || check.type == VARIABLE){
					okExpression = false;
					break;
				}
				if(check.type == OPERATION)
					if(check.content.operation == UN_MINUS)
						check_un_minus = 0;
                push(result, curToken);
                break;
            case LBR:
				if(check.type == NUMBER || check.type == VARIABLE){
					okExpression = false;
					break;
				}
				if(check.type == OPERATION)
					if(check.content.operation == UN_MINUS)
						check_un_minus = 0;
                push(tmp, curToken);
                break;
            case RBR:
				if(check.type == OPERATION || check.type == LBR){
					okExpression = false;
					break;
				}
                while (!isStackEmpty(tmp)) {
                    topToken = pop(tmp);
                    if (topToken.type == LBR) {
                        break;
                    }
                    push(result, topToken);
                }
                if (topToken.type != LBR) {
					okExpression = false;
                }
                break;
            case OPERATION:
				if(curToken.content.operation == UN_MINUS)
					check_un_minus = 1;
				if((check.type == OPERATION || check.type == LBR || check.type == NONE) && curToken.content.operation != UN_MINUS){
					okExpression = false;
					break;
				}
                if (isStackEmpty(tmp)) {
                    topToken.type = NONE;
                } else {
                    topToken = pop(tmp);
                }
				while(topToken.type != NONE && topToken.type != LBR 
				   && forcePush(topToken.content.operation, curToken.content.operation)){
					push(result, topToken);
					if(isStackEmpty(tmp)){
						topToken.type = NONE;
						break;
					}
					topToken = pop(tmp);
				}
				if(topToken.type != NONE)
					push(tmp, topToken);
				
				push(tmp, curToken);
				break;
			default:
				printf("Неопознанный тип токена\n");
        }
    }

	if(okExpression){
		while (!isStackEmpty(tmp)) {
			Token curToken = pop(tmp);
			if (curToken.type == LBR) {
				okExpression = false;
				break;
			}
			push(result, curToken);
		}
		deleteStack(tmp);
		free(tmp);
	}
	
	if (!okExpression || check_un_minus){
		printf("Ошибка при вводе!\n");
		deleteStack(tmp);
		free(tmp);
		deleteStack(result);
	}

    return result;
}

typedef struct Treenode Treenode;

struct Treenode {
    Token value;
    Treenode *l, *r;
};

Treenode* makeNode(Token val) {
    Treenode *node = malloc(sizeof(*node));
    node->value = val;
    node->l = node->r = NULL;
    return node;
}

Treenode* buildTree(Stack *expression, Treenode* root) {
	Treenode *tmp = NULL;
	if(!isStackEmpty(expression)){
		Token topToken = pop(expression);
		tmp = makeNode(topToken);
		if(topToken.type == OPERATION){
			tmp->l = buildTree(expression, tmp->l);
			if(topToken.content.operation != UN_MINUS)
				tmp->r = buildTree(expression, tmp->r);
		}
		return tmp;
	}
	return NULL;
}

void printTree(Treenode* current, int d){
	if (current->r != NULL) {
		printTree(current->r, d + 1);
    }
	TOKEN_TYPE type = current->value.type;
	switch(type){
		case NUMBER:
			printf("%*s%lf\n", 4 * d, " ", current->value.content.number);
			break;
		case VARIABLE:
			printf("%*s%s\n", 4 * d, " ", current->value.content.name);
			break;
		case OPERATION:
			printf("%*s%c\n", 4 * d, " ", current->value.content.operation);
			break;
		default:
			printf("Ошибка при вводе!\n");
	}
	if (current->l != NULL) {
	printTree(current->l, d + 1);
	}
}

void printExpression(Treenode *current, Treenode *save) {
    if (current->r != NULL) {
		if(current->value.type == OPERATION){
			if(current->value.content.operation == PLUS || current->value.content.operation == MINUS ||
			   current->value.content.operation == POWER)
				if(current != save)
					printf("(");
		}
        printExpression(current->r, save);
    }
	TOKEN_TYPE type = current->value.type;
    switch (type) {
        case NUMBER:
			printf("%.2lf", current->value.content.number);
			break;
		case VARIABLE:
            printf("%s", current->value.content.name);
            break;
		case OPERATION:
			if (current->value.content.operation == UN_MINUS){
				if(current != save)
					printf("(");
			}
            printf("%c", current->value.content.operation);
			break;
		default:
			printf("Ошибка при вводе!\n");
        }
    if (current->l != NULL) {
        printExpression(current->l, save);
		if(current->value.type == OPERATION){
			if(current->value.content.operation == PLUS || current->value.content.operation  == MINUS 
			|| current->value.content.operation == UN_MINUS || current->value.content.operation == POWER)
				if(current != save)
					printf(")");
		}
    }
}

void deleteTree(Treenode* current) {
    if (current->l != NULL) {
        deleteTree(current->l);
		free(current->l);
		current->l = NULL;
    }
    if (current->r != NULL) {
        deleteTree(current->r);
		free(current->r);
        current->r = NULL;		
    }
}

void add_childs_to_node(Treenode *node, Treenode *need_to_add){
	if(need_to_add->l != NULL)
		node->l = makeNode(need_to_add->l->value);
	if(need_to_add->r != NULL)
		node->r = makeNode(need_to_add->r->value);
	
	if(need_to_add->l != NULL)
		if(need_to_add->l->value.type == OPERATION)
			add_childs_to_node(node->l, need_to_add->l);
	
	if(need_to_add->r != NULL)
		if(need_to_add->r->value.type == OPERATION)
			add_childs_to_node(node->r, need_to_add->r);
}

int CheckNode_forTask(Treenode* root){
	if(root == NULL)
		return 0;
	if(root->l == NULL || root->r == NULL)
		return 0;
	
	if(root->value.content.operation == MULT){
		if(root->r->value.type == VARIABLE && root->l->value.type == OPERATION)
		    {
			if(root->l->value.content.operation == PLUS || root->l->value.content.operation == UN_MINUS){
				Treenode* tmpl = root->l;
				while(tmpl->value.type == OPERATION){
					if(tmpl->value.content.operation != UN_MINUS)
						break;
					tmpl = tmpl->l;
				}
				if(tmpl->value.type != NUMBER || tmpl->value.type != VARIABLE){
					if(tmpl->value.content.operation == PLUS)
						return 1;
				}
			}
		} else if(root->l->value.type == VARIABLE && root->r->value.type == OPERATION){
			if(root->r->value.content.operation == PLUS || root->r->value.content.operation == UN_MINUS){
				Treenode* tmpr = root->r;
				while(tmpr->value.type == OPERATION){
					if(tmpr->value.content.operation != UN_MINUS)
						break;
					tmpr = tmpr->l;
				}
				if(tmpr->value.type != NUMBER || tmpr->value.type != VARIABLE){
					if(tmpr->value.content.operation == PLUS)
						return 2;
				}
			}
			
		} else if(root->r->value.type == OPERATION && root->l->value.type == OPERATION){
			if(((root->r->value.content.operation == POWER || root->r->value.content.operation == UN_MINUS 
			 ||  root->r->value.content.operation == MULT || root->r->value.content.operation == DIVIDE) 
			 && (root->l->value.content.operation == PLUS || root->l->value.content.operation == UN_MINUS))
		     ||((root->l->value.content.operation == POWER || root->l->value.content.operation == UN_MINUS
			 ||  root->l->value.content.operation == MULT || root->l->value.content.operation == DIVIDE)
			 && (root->r->value.content.operation == PLUS || root->r->value.content.operation == UN_MINUS))
			 || (root->r->value.content.operation == POWER && (root->l->value.content.operation == MULT 
			 ||  root->l->value.content.operation == DIVIDE))
			 || (root->l->value.content.operation == POWER && (root->r->value.content.operation == MULT 
			 ||  root->r->value.content.operation == DIVIDE))){
				 
				Treenode* tmpl = root->l;
				while(tmpl->value.type == OPERATION){
					if(tmpl->value.content.operation != UN_MINUS)
						break;
					tmpl = tmpl->l;
				}
				if(tmpl->value.type != NUMBER || tmpl->value.type != VARIABLE){
					if(tmpl->value.content.operation == PLUS || tmpl->value.content.operation == MULT){
						if(tmpl->value.content.operation == MULT){
							if(!CheckNode_forTask(tmpl))
								return 0;
						}
						return 1;
					}
				}
				
				Treenode* tmpr = root->r;
				while(tmpr->value.type == OPERATION){
					if(tmpr->value.content.operation != UN_MINUS)
						break;
					tmpr = tmpr->l;
				}
				if(tmpr->value.type != NUMBER || tmpr->value.type != VARIABLE){
					if(tmpr->value.content.operation == PLUS || tmpr->value.content.operation == MULT){
						if(tmpr->value.content.operation == MULT){
							if(!CheckNode_forTask(tmpr))
								return 0;
						}
						return 2;
					}
				}
			}
		}
	}
	return 0;
}



Treenode* CheckTree_forTask(Treenode* node){
	if(CheckNode_forTask(node))
		return node;
	
	Treenode* tmp;
	
	if(node->r != NULL){
		tmp = CheckTree_forTask(node->r);
		if(tmp != NULL)
			return tmp;
	}
		
	if(node->l != NULL){
		tmp = CheckTree_forTask(node->l);
		if(tmp != NULL)
			return tmp;
	}
	
	return NULL;
}

void TaskTree(Treenode *root){
	Treenode *tmp = root;
	
	while(tmp != NULL){
		int check = CheckNode_forTask(tmp);
		Treenode *save;
		Treenode *save_tmp;
		Treenode *save_l;
		Treenode *save_r;
		
			switch(check){
 
				case 1:
					if(tmp->l->r == NULL){
						save = makeNode(tmp->l->value);
						save_tmp = tmp->l->l;
						save_l = save;
						save_r = save;
						while(save_tmp->r == NULL){
							save_l->l = makeNode(save_tmp->value);
							if(save_l == save)
								save->r = makeNode(save_tmp->value);
							else save_r->l = makeNode(save_tmp->value);
							if(save_l != save)
								save_r = save_r->l;
							else save_r = save->r;
							save_l = save_l->l;
							save_tmp = save_tmp->l;
						}
						if(save_tmp->value.content.operation == MULT){
							tmp = save_tmp;
							deleteTree(save);
							free(save);
							continue;
						}
						save_l->l = makeNode(save_tmp->l->value);
						add_childs_to_node(save_l->l, save_tmp->l);
						if(save_l == save_r){
							save_r->r = makeNode(save_tmp->r->value);
							add_childs_to_node(save_r->r, save_tmp->r);
						}
						else {
							save_r->l = makeNode(save_tmp->r->value);
							add_childs_to_node(save_r->l, save_tmp->r);
						}
						deleteTree(tmp->l);
						tmp->l->l = makeNode(save->value);
						tmp->l->r = makeNode(save->value);
						tmp->l->l->l = makeNode(save->l->value);
						tmp->l->r->l = makeNode(save->r->value);
						add_childs_to_node(tmp->l->l->l, save->l);
						add_childs_to_node(tmp->l->r->l, save->r);
						deleteTree(save);
						free(save);
					}
					if(tmp->l->value.content.operation == MULT){
						tmp = tmp->l;
						continue;
					}
					save = makeNode(tmp->r->value);
					add_childs_to_node(save, tmp->r);
					deleteTree(tmp->r);
					tmp->r->r = makeNode(save->value);
					add_childs_to_node(tmp->r->r, save);
					tmp->r->l = makeNode(tmp->l->r->value);
					if(tmp->l->r->value.type == OPERATION){
						add_childs_to_node(tmp->r->l, tmp->l->r);
						deleteTree(tmp->l->r);
					}
					free(tmp->l->r);
					tmp->l->r = makeNode(save->value);
					add_childs_to_node(tmp->l->r, save);
					break;
					
				case 2:
					if(tmp->r->r == NULL){
						save = makeNode(tmp->r->value);
						save_tmp = tmp->r->l;
						save_l = save;
						save_r = save;
						while(save_tmp->r == NULL){
							save_l->l = makeNode(save_tmp->value);
							if(save_l == save)
								save->r = makeNode(save_tmp->value);
							else save_r->l = makeNode(save_tmp->value);
							if(save_l != save)
								save_r = save_r->l;
							else save_r = save->r;
							save_l = save_l->l;
							save_tmp = save_tmp->l;
						}
						if(save_tmp->value.content.operation == MULT){
							tmp = save_tmp;
							deleteTree(save);
							free(save);
							continue;
						}
						save_l->l = makeNode(save_tmp->l->value);
						add_childs_to_node(save_l->l, save_tmp->l);
						if(save_l == save_r){
							save_r->r = makeNode(save_tmp->r->value);
							add_childs_to_node(save_r->r, save_tmp->r);
						}
						else {
							save_r->l = makeNode(save_tmp->r->value);
							add_childs_to_node(save_r->l, save_tmp->r);
						}
						deleteTree(tmp->r);
						tmp->r->l = makeNode(save->value);
						tmp->r->r = makeNode(save->value);
						tmp->r->l->l = makeNode(save->l->value);
						tmp->r->r->l = makeNode(save->r->value);
						add_childs_to_node(tmp->r->l->l, save->l);
						add_childs_to_node(tmp->r->r->l, save->r);
						deleteTree(save);
						free(save);
					}
					if(tmp->r->value.content.operation == MULT){
						tmp = tmp->r;
						continue;
					}
					save = makeNode(tmp->l->value);
					add_childs_to_node(save, tmp->l);
					deleteTree(tmp->l);
					tmp->l->l = makeNode(save->value);
					add_childs_to_node(tmp->l->l, save);
					tmp->l->r = makeNode(tmp->r->l->value);
					if(tmp->r->l->value.type == OPERATION){
						add_childs_to_node(tmp->l->r, tmp->r->l);
						deleteTree(tmp->r->l);
					}
					free(tmp->r->l);
					tmp->r->l = makeNode(save->value);
					add_childs_to_node(tmp->r->l, save);
					break;
			
			}
		if(check){
			if(tmp->value.type != OPERATION)
				tmp->value.type = OPERATION;
			tmp->value.content.operation = PLUS;
			if(tmp->l->value.type != OPERATION)
				tmp->l->value.type = OPERATION;
			if(tmp->r->value.type != OPERATION)
				tmp->r->value.type = OPERATION;
			tmp->l->value.content.operation = tmp->r->value.content.operation = MULT;
			deleteTree(save);
			free(save);
			
		}
		tmp = CheckTree_forTask(root);
	}
}

int main(){
	Stack *s = NULL;
	Treenode *root = NULL;
	int d = 0;
	
	s = initStack();
	printf("Программа преобразовывает произведение переменной на сумму в сумму прозведений\nВведите выражение:\n");
	s = readAndConvertExpression(s);
	printf("ReversedPolish:\n");
	printReversePolish(s);
	printf("\n");
	if(s->head != NULL){
		root = buildTree(s, root);
		printf("Исходное дерево:\n");
		printTree(root, d);
		printf("\n\nВыражение:\n");
		printExpression(root,root);
		printf("\n");
		if(CheckTree_forTask(root) != NULL){
			printf("\nМеняем выражение по заданию:\n");
			printExpression(root,root);
			printf(" <=> ");
			TaskTree(root);
			printExpression(root,root);
			printf("\n\n");		
			printf("Изменённое дерево:\n");
			printTree(root,d);
			printf("\n");
		}			
	}

	if(s->head != NULL)
		deleteStack(s);
	
	if(root != NULL)
		deleteTree(root);
	

	free(root);
	free(s);

	return 0;
}
