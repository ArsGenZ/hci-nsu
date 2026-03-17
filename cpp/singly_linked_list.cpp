#include <iostream>

using namespace std;

// Структура узла односвязного списка
struct Node {
    int data;
    Node* next;

    Node(int val) : data(val), next(nullptr) {}
};

//Функции управления списком
void clearList(Node*& head);

// 1. Создать пустой список
void createList(Node*& head) {
    clearList(head);
    cout << "Пустой список создан." << endl;
}

// Поиск элемента по значению
bool searchElement(Node* head, int value) {
    Node* current = head;
    while (current != nullptr) {
        if (current->data == value) {
            return true;
        }
        current = current->next;
    }
    return false;
}

// 2. Добавить элемент (упорядоченно, без дубликатов)
void addElement(Node*& head, int value) {
    if (searchElement(head, value)) {
        cout << "Элемент " << value << " уже существует в списке. Добавление отменено." << endl;
        return;
    }

    Node* newNode = new Node(value);

    // Если список пуст или новое значение меньше первого элемента
    if (head == nullptr || head->data > value) {
        newNode->next = head;
        head = newNode;
    } else {
        // Поиск места для вставки
        Node* current = head;
        while (current->next != nullptr && current->next->data < value) {
            current = current->next;
        }
        // Вставка между current и current->next
        newNode->next = current->next;
        current->next = newNode;
    }
    cout << "Элемент " << value << " успешно добавлен." << endl;
}

// 3. Удалить элемент по значению
void removeElement(Node*& head, int value) {
    if (head == nullptr) {
        cout << "Список пуст." << endl;
        return;
    }

    if (head->data == value) {
        Node* temp = head;
        head = head->next;
        delete temp;
        cout << "Элемент " << value << " удален." << endl;
        return;
    }

    Node* current = head;
    while (current->next != nullptr && current->next->data != value) {
        current = current->next;
    }

    if (current->next != nullptr) {
        Node* temp = current->next;
        current->next = current->next->next;
        delete temp;
        cout << "Элемент " << value << " удален." << endl;
    } else {
        cout << "Элемент " << value << " не найден в списке." << endl;
    }
}

// 5. Вывод списка
void printList(Node* head) {
    if (head == nullptr) {
        cout << "Список пуст." << endl;
        return;
    }

    cout << "Содержимое списка: ";
    Node* current = head;
    while (current != nullptr) {
        cout << current->data;
        if (current->next != nullptr) {
            cout << " -> ";
        }
        current = current->next;
    }
    cout << endl;
}

// Освобождение памяти (очистка списка)
void clearList(Node*& head) {
    while (head != nullptr) {
        Node* temp = head;
        head = head->next;
        delete temp;
    }
    cout << "Память освобождена." << endl;
}

// --- Функция меню ---
void showMenu() {
    cout << "\n--- Меню ---" << endl;
    cout << "1. Создать пустой список" << endl;
    cout << "2. Добавить элемент" << endl;
    cout << "3. Удалить элемент" << endl;
    cout << "4. Поиск элемента" << endl;
    cout << "5. Вывод списка" << endl;
    cout << "6. Выход" << endl;
    cout << "Выберите действие: ";
}

int main() {
    // Инициализация списка
    // Node* head = nullptr;
    // int choice;
    // int value;

    setlocale(LC_ALL, "Russian");

    // do {
    //     showMenu();
    //     if (!(cin >> choice)) {
    //         cin.clear();
    //         cin.ignore(32767, '\n');
    //         cout << "Неверный ввод. Попробуйте снова." << endl;
    //         continue;
    //     }

    //     switch (choice) {
    //         case 1:
    //             createList(head);
    //             break;
    //         case 2:
    //             cout << "Введите число для добавления: ";
    //             cin >> value;
    //             addElement(head, value);
    //             break;
    //         case 3:
    //             cout << "Введите число для удаления: ";
    //             cin >> value;
    //             removeElement(head, value);
    //             break;
    //         case 4:
    //             cout << "Введите число для поиска: ";
    //             cin >> value;
    //             if (searchElement(head, value)) {
    //                 cout << "Элемент " << value << " найден." << endl;
    //             } else {
    //                 cout << "Элемент " << value << " не найден." << endl;
    //             }
    //             break;
    //         case 5:
    //             printList(head);
    //             break;
    //         case 6:
    //             cout << "Выход из программы..." << endl;
    //             break;
    //         default:
    //             cout << "Неверный номер пункта меню." << endl;
    //     }

    // } while (choice != 6);



// # 1 Task
    Node* head = nullptr;
    int value;
    do
    {
        if (!(cin >> value)) {
                cin.clear();
                cin.ignore(32767, '\n');
                break;;
            }

        addElement(head,value);
    }while (true);

    printList(head);
    Node* current = head;
    int count = 0;
    while (current != nullptr){
        if (current->data < 0 && current->data % 7 == 0)
            count++;
        current = current->next;
    }
    cout << count << endl;
    clearList(head);

    return 0;



//     Node* head = nullptr;
//     int value;
//     int arithmetic_mean;
//     do
//     {
//         if (!(cin >> value)) {
//                 cin.clear();
//                 cin.ignore(32767, '\n');
//                 break;;
//             }

//         Node* newNode = new Node(value);
//         Node* current = head;
//         int count = 0;
//         int temp = 0;
//         while (current->next != nullptr) {
//             current = current->next;
//             count++;
//             temp += current->data;
//         }
//         // Вставка между current и current->next
//         newNode->next = current->next;
//         current->next = newNode;
//         arithmetic_mean = (temp + value) / (count + 1);
//     }while (true);

//     printList(head);
//     cout << arithmetic_mean << endl;
//     clearList(head);

//     return 0;
// }
