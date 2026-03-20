#include <iostream>

using namespace std;

// Структура узла двусвязного списка
struct Node {
    int value;
    Node* next;
    Node* prev;
};

int main() {

    int N, K;

    // Ввод данных с клавиатуры
    if (!(cin >> N >> K)) {
        return 0;
    }

    Node* head = nullptr;
    Node* tail = nullptr;

    for (int i = 1; i <= N; ++i) {
        Node* newNode = new Node;
        newNode->value = i;
        newNode->next = nullptr;
        newNode->prev = nullptr;

        if (head == nullptr) {
            head = newNode;
            tail = newNode;
        } else {
            tail->next = newNode;
            newNode->prev = tail;
            tail = newNode;
        }
    }

    if (head != nullptr) {
        tail->next = head;
        head->prev = tail;
    }

    Node* current = head;

    while (N > 1) {
        for (int i = 0; i < K - 1; ++i) {
            current = current->next;
        }

        // Связываем соседей удаляемого элемента
        current->prev->next = current->next;
        current->next->prev = current->prev;

        // Запоминаем следующий элемент
        Node* nextNode = current->next;

        delete current;

        current = nextNode;

        N--;
    }

    cout << current->value << endl;

    delete current;

    return 0;
}
