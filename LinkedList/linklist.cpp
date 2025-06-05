#include<iostream>
#include <vector>
#include <sstream>
#include <math.h>
#include "linklist.h"
#include "visualize_autogen.cpp"

int main(){
    Node* head = new Node(1);
    Node* current = head;
    for (int i = 2; i <= 100; i++) {
        current->next = new Node(i);
        current = current->next;
    }
    
    visualize(head);
}