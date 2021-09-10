#ifndef __BIN_TREE__
#define __BIN_TREE__

#include <iostream>
#include <vector>

class Tree {
public:
    struct Node{
    Node(int id_): id(id_){}
    int id;
    Node *left = nullptr;
    Node *right = nullptr;
    };

    Node *head = nullptr;
public:
    Tree() = default;
    ~Tree(){
        this->destroy(this->head);
    }

    std::vector<int> get_path_to(int& id, Node* node=nullptr) {
        std::vector<int> path;
        if (node == nullptr)
            node = this->head;
        this->find_path(node, id, path);
        return path;
    }

    bool is_contains(Node *node, int id){
        bool res;
        if(node == nullptr){
            res = false;
        }
        else if(id == node->id){
            res = true;
        }
        else if(id < node->id){
            res = is_contains(node->left, id);
        }
        else if(id > node->id){
            res = is_contains(node->right, id);
        }
        return res;
    }

    void insert(int& id){
        if(this->head == nullptr){
            this->head = new Node(id);
            this->head->left = nullptr;
            this->head->right = nullptr;
            return;
        }
        Node* tmp = this->head;
        while(tmp != nullptr){
            if(id < tmp->id){
                if(tmp->left == nullptr){
                    tmp->left = new Node(id);          
                    tmp->left->left = nullptr;
                    tmp->left->right = nullptr;
                    break;
                }
                tmp = tmp->left;
            }
            else if(id > tmp->id){
                if(tmp->right == nullptr){
                    tmp->right = new Node(id);
                    tmp->right->left = nullptr;
                    tmp->right->right = nullptr;
                    return;
                }
                tmp = tmp->right;
            }
        }
    }

    void erase(int& id){
        Node* prev = nullptr;
        Node* tmp = this->head;
        while(tmp != nullptr){
            if (id == tmp->id) {
                if (prev == nullptr) {
                    this->head = nullptr;
                } else {
                    if (prev->left == tmp) {
                        prev->left = nullptr;
                    } else {
                        prev->right = nullptr;
                    }
                }
                destroy(tmp);
            } else if(id < tmp->id) {
                prev = tmp;
                tmp = tmp->left;
            } else if(id > tmp->id) {
                prev = tmp;
                tmp = tmp->right;
            }
        }
    }

    void find_path(Node* node, int& id, std::vector<int>& path) {
        while(node != nullptr){
            path.push_back(node->id);
            if(node->id == id)
                break;
            else if(id > node->id)
                node = node->right;
            else if(id < node->id)
                node = node->left;
        }
    }

    void destroy(Node* node){
        if(node == nullptr)
            return;
        destroy(node->right);
        destroy(node->left);
        delete node;
    }
};
#endif 
