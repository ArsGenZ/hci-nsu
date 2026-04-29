template <typename T>
struct Node {
    T data;
    Node* next;

    explicit Node(T val) : data(val), next(nullptr) {}
    };

template <typename T>
class Stack {
private:
    Node<T>* topNode;
    int size;

public:
    Stack() {
        topNode = nullptr;
        size = 0;
    }

    ~Stack() {
        while (!isEmpty())
            pop();
    }

    void push(T x) {
        Node<T>* newNode = new Node<T>(x);
        newNode->next = topNode;
        topNode = newNode;
        size++;
    }

    T pop() {
        Node<T>* temp = topNode;
        T value = temp->data;
        topNode = topNode->next;
        delete temp;
        size--;
        return value;
    }

    T peek() {
        return topNode->data;
    }

    bool isEmpty() {
        return (topNode == nullptr);
    }

    int getSize() {
        return size;
    }
};
