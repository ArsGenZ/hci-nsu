#include <iostream>
#include <string>
#include <cctype>
#include <limits>

using namespace std;

// Узел односвязного списка
// Хранит значение и указатель на следующий узел
template <typename T>
struct Node {
    T data;           // Данные узла
    Node<T>* next;    // Указатель на следующий узел

    // Конструктор узла
    Node(T value) : data(value), next(nullptr) {}
};

// Шаблонный класс Стека на основе односвязного списка
template <typename T>
class Stack {
private:
    Node<T>* topNode;  // Указатель на верхний элемент стека
    int size;          // Текущее количество элементов

public:
    // 1. Создать стек (Конструктор)
    // Аналог функции create(*s)
    Stack() {
        topNode = nullptr;  // Изначально стек пуст
        size = 0;
        cout << "Стек создан." << endl;
    }

    // Деструктор - очищает память при удалении стека
    ~Stack() {
        while (!isEmpty()) {
            pop();
        }
        cout << "Стек удален, память освобождена." << endl;
    }

    // 2. Добавить элемент в стек
    // Аналог функции push(*s, x)
    void push(T x) {
        Node<T>* newNode = new Node<T>(x);  // Создаем новый узел
        newNode->next = topNode;            // Новый узел указывает на старый верх
        topNode = newNode;                  // Верх теперь новый узел
        size++;
        cout << "Элемент " << x << " добавлен в стек." << endl;
    }

    // 3. Извлечь элемент из стека
    // Аналог функции pop(*s)
    T pop() {
        if (isEmpty()) {
            cout << "Ошибка: Стек пуст (Stack Underflow)!" << endl;
            return T();  // Возвращаем значение по умолчанию
        }

        Node<T>* temp = topNode;      // Запоминаем текущий верх
        T value = temp->data;         // Сохраняем данные
        topNode = topNode->next;      // Перемещаем верх на следующий узел
        delete temp;                  // Освобождаем память старого верха
        size--;

        cout << "Элемент " << value << " удален из стека." << endl;
        return value;
    }

    // 4. Посмотреть значение на верхушке
    // Аналог функции peek(*s)
    T peek() {
        if (isEmpty()) {
            cout << "Ошибка: Стек пуст!" << endl;
            return T();
        }
        return topNode->data;
    }

    // 5. Проверка на пустоту
    // Аналог функции empty(*s)
    bool isEmpty() {
        return (topNode == nullptr);
    }

    // Вспомогательная функция для получения размера
    int getSize() {
        return size;
    }
};

// меню стека
void showStackMenu() {
    cout << "\n========== МЕНЮ СТЕКА ==========" << endl;
    cout << "1. Push (Добавить элемент)" << endl;
    cout << "2. Pop (Удалить и показать элемент)" << endl;
    cout << "3. Peek (Показать верхний элемент)" << endl;
    cout << "4. Empty (Проверить, пуст ли стек)" << endl;
    cout << "0. Выход" << endl;
    cout << "=================================" << endl;
    cout << "Выберите действие: ";
}


// Конвертер инфиксной записи в постфиксную
class InfixToPostfix {
private:
    int getPriority(char op) {
        switch (op) {
            case '(': return 1;
            case ')': return 2;
            case '=': return 3;
            case '+':
            case '-': return 4;
            case '*':
            case '/': return 5;
            default: return 0;
        }
    }

    bool isOperator(char c) {
        return (c == '+' || c == '-' || c == '*' || c == '/' || c == '=' || c == '(' || c == ')');
    }

    bool isOperand(char c) {
        return isalnum(c);
    }

public:
    string convert(string infix) {
        Stack<char> opStack;
        string postfix = "";

        for (size_t i = 0; i < infix.length(); i++) {
            char X = infix[i];

            if (X == ' ') {
                continue;
            }

            if (isOperand(X)) {
                postfix += X;
                if (i + 1 < infix.length() && !isOperand(infix[i + 1])) {
                    postfix += ' ';
                }
            }
            else if (X == '(') {
                opStack.push(X);
            }
            else if (X == ')') {
                while (!opStack.isEmpty() && opStack.peek() != '(') {
                    postfix += opStack.pop();
                    postfix += ' ';
                }
                if (!opStack.isEmpty() && opStack.peek() == '(') {
                    opStack.pop();
                }
            }
            else if (isOperator(X)) {
                while (!opStack.isEmpty() &&
                       getPriority(opStack.peek()) >= getPriority(X) &&
                       opStack.peek() != '(') {
                    postfix += opStack.pop();
                    postfix += ' ';
                }
                opStack.push(X);
            }
        }

        while (!opStack.isEmpty()) {
            char op = opStack.pop();
            if (op != '(' && op != ')') {
                postfix += op;
                postfix += ' ';
            }
        }

        return postfix;
    }
};

// Класс для вычисления постфиксного выражения #3
class PostfixEvaluator {
private:
    Stack<double> evalStack;
    bool hasError;

    bool isOperator(char c) {
        return (c == '+' || c == '-' || c == '*' || c == '/' || c == '=');
    }

    double applyOperation(double op2, double op1, char op) {
        switch (op) {
            case '+': return op1 + op2;
            case '-': return op1 - op2;
            case '*': return op1 * op2;
            case '/':
                if (op2 == 0) {
                    cout << "Ошибка: Деление на ноль!" << endl;
                    hasError = true;
                    return 0;
                }
                return op1 / op2;
            case '=': return op2;
            default: return 0;
        }
    }

public:
    PostfixEvaluator() : hasError(false) {}

    double evaluate(string postfix) {
        evalStack = Stack<double>();
        hasError = false;

        string currentNumber = "";

        for (size_t i = 0; i < postfix.length(); i++) {
            char X = postfix[i];

            if (X == ' ') {
                if (!currentNumber.empty()) {
                    double num = stod(currentNumber);
                    evalStack.push(num);
                    currentNumber = "";
                }
                continue;
            }

            if (isOperator(X)) {
                if (!currentNumber.empty()) {
                    double num = stod(currentNumber);
                    evalStack.push(num);
                    currentNumber = "";
                }

                if (evalStack.getSize() < 2) {
                    cout << "Ошибка: Недостаточно операндов для операции!" << endl;
                    hasError = true;
                    return 0;
                }

                double op2 = evalStack.pop();
                double op1 = evalStack.pop();
                double result = applyOperation(op2, op1, X);

                if (hasError) {
                    return 0;
                }

                evalStack.push(result);
            }
            else if (isdigit(X) || X == '.') {
                currentNumber += X;
            }
        }

        if (!currentNumber.empty()) {
            double num = stod(currentNumber);
            evalStack.push(num);
        }

        if (hasError) {
            return 0;
        }

        if (evalStack.getSize() != 1) {
            cout << "Ошибка: Некорректное выражение!" << endl;
            return 0;
        }

        return evalStack.pop();
    }
};

// меню Конвертера
void showConvertMenu() {
    cout << "\n========== ГЛАВНОЕ МЕНЮ ==========" << endl;
    cout << "1. Конвертировать инфикс → постфикс" << endl;
    cout << "2. Вычислить постфиксное выражение" << endl;
    cout << "3. Полный цикл: Конвертация + Вычисление" << endl;
    cout << "0. Выход" << endl;
    cout << "===================================" << endl;
    cout << "Выберите действие: ";
}

void clearInputBuffer() {
    cin.clear();
    cin.ignore(numeric_limits<streamsize>::max(), '\n');
}



// #1
// int main() {
//     // Создаем стек для целых чисел
//     // Здесь вызывается функция create (конструктор)
//     Stack<int> myStack;

//     int choice;
//     int value;

//     while (true) {
//         showStackMenu();
//         cin >> choice;

//         switch (choice) {
//             case 1: // Push
//                 cout << "Введите число для добавления: ";
//                 cin >> value;
//                 myStack.push(value);
//                 break;

//             case 2: // Pop
//                 value = myStack.pop();
//                 break;

//             case 3: // Peek
//                 value = myStack.peek();
//                 if (!myStack.isEmpty()) {
//                     cout << "Верхний элемент: " << value << endl;
//                 }
//                 break;

//             case 4: // Empty
//                 if (myStack.isEmpty())
//                     cout << "Стек пуст." << endl;
//                 else
//                     cout << "Стек не пуст. Текущий размер: " << myStack.getSize() << endl;
//                 break;

//             case 0: // Exit
//                 cout << "Завершение работы." << endl;
//                 return 0;

//             default:
//                 cout << "Неверный ввод. Попробуйте снова." << endl;
//         }
//     }

//     return 0;
// }

// #2
int main() {

    setlocale(LC_ALL, "Russian");

    InfixToPostfix converter;
    PostfixEvaluator evaluator;
    int choice;
    string infix, postfix;
    double result;

    cout << "=== Конвертер инфиксной формы в постфиксную ===" << endl;
    cout << "Приоритеты операций:" << endl;
    cout << "  (  )  =  + -  * /" << endl;
    cout << "  1  2  3  4   5" << endl;

    while (true) {
        showConvertMenu();

        if (!(cin >> choice)) {
            cout << "Ошибка ввода! Введите число." << endl;
            clearInputBuffer();
            continue;
        }

        switch (choice) {
            case 1:
                cout << "\nВведите арифметическое выражение в инфиксной форме:" << endl;
                cout << "Пример: (a+b)*c или 5+3*2" << endl;
                cout << "> ";
                clearInputBuffer();  // Очищаем буфер перед getline
                getline(cin, infix);

                if (infix.empty()) {
                    cout << "Ошибка: пустая строка!" << endl;
                    break;
                }

                postfix = converter.convert(infix);

                cout << "\n********** РЕЗУЛЬТАТ **********" << endl;
                cout << "Инфиксная форма:  " << infix << endl;
                cout << "Постфиксная форма: " << postfix << endl;
                cout << "********************************" << endl;
                break;

            case 2:
                cout << "\n--- Вычислитель постфиксных выражений ---" << endl;
                cout << "Введите выражение в постфиксной форме:" << endl;
                cout << "Важно: разделяйте числа пробелами!" << endl;
                cout << "Пример: 5 3 + или 2 3 4 * +" << endl;
                cout << "> ";
                clearInputBuffer();
                getline(cin, postfix);

                if (postfix.empty()) {
                    cout << "Ошибка: пустая строка!" << endl;
                    break;
                }

                result = evaluator.evaluate(postfix);

                cout << "\n********** РЕЗУЛЬТАТ **********" << endl;
                cout << "Выражение: " << postfix << endl;
                cout << "Результат: " << result << endl;
                cout << "********************************" << endl;
                break;

                case 3:
                    cout << "\n=== ПОЛНЫЙ ЦИКЛ: Конвертация + Вычисление ===" << endl;
                    cout << "Введите выражение в инфиксной форме:" << endl;
                    cout << "Пример: (5+3)*2" << endl;
                    cout << "> ";
                    clearInputBuffer();
                    getline(cin, infix);

                    if (infix.empty()) {
                        cout << "Ошибка: пустая строка!" << endl;
                        break;
                    }

                    // Шаг 1: Конвертация
                    postfix = converter.convert(infix);
                    cout << "\n[Шаг 1] Постфиксная форма: " << postfix << endl;

                    // Шаг 2: Вычисление
                    result = evaluator.evaluate(postfix);
                    cout << "\n[Шаг 2] Результат вычисления: " << result << endl;

                    cout << "\n********** ИТОГ **********" << endl;
                    cout << "Инфикс:     " << infix << endl;
                    cout << "Постфикс:   " << postfix << endl;
                    cout << "Результат:  " << result << endl;
                    cout << "**************************" << endl;
                    break;

            case 0:
                cout << "Завершение работы." << endl;
                return 0;

            default:
                cout << "Неверный ввод. Попробуйте снова." << endl;
        }
    }

    return 0;
}
