class Node{
    public:
    int data;
    Node* next;
    Node* prev;
    Node(int num){
        data = num;
        next = NULL;
        prev = NULL;
    }
    ~Node(){
        delete next;
        delete prev;
    }
};