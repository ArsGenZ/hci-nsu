#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <algorithm>
#include <cctype>
#include "SteckClass.cpp"

struct TreeNode {
    std::string word;
    TreeNode* left;
    TreeNode* right;

    explicit TreeNode(std::string w) : word(std::move(w)), left(nullptr), right(nullptr) {}
};

std::string toLowerChar(const std::string& str) {
    std::string result = str;
    for (char& c : result) {
        c = std::tolower(static_cast<unsigned char>(c));
    }
    return result;
}

TreeNode* buildBalancedBST(const std::vector<std::string>& words, int start, int end) {
    if (start > end)
        return nullptr;

    int mid = start + (end - start) / 2;
    TreeNode* node = new TreeNode(words[mid]);

    node->left = buildBalancedBST(words, start, mid - 1);
    node->right = buildBalancedBST(words, mid + 1, end);

    return node;
}

int getTreeHeight(TreeNode* root) {
    if (!root) return 0;
    int leftH  = getTreeHeight(root->left);
    int rightH = getTreeHeight(root->right);
    return 1 + std::max(leftH, rightH);
}

void printTreeRecursive(TreeNode* root, int space) {
    if (!root) return;

    space += 12; // Отступ между уровнями (в пробелах)

    // 1. Сначала печатаем правое поддерево (в консоли будет СВЕРХУ)
    printTreeRecursive(root->right, space);

    // 2. Печатаем текущий узел с отступом
    std::cout << '\n';
    for (int i = 12; i < space; i++)
        std::cout << ' ';
    std::cout << root->word << std::endl;

    // 3. Затем печатаем левое поддерево (в консоли будет СНИЗУ)
    printTreeRecursive(root->left, space);
}

void printTree(TreeNode* root) {
    if (!root) {
        std::cout << "(дерево пусто)" << std::endl;
        return;
    }
    printTreeRecursive(root, 0);
}

void inorderTraversal(TreeNode* root, std::ofstream& out) {
    Stack<TreeNode*> stack;
    TreeNode* current = root;

    while (current != nullptr || !stack.isEmpty()) {
        // 1. Идём влево до конца, складывая узлы в стек
        while (current != nullptr) {
            stack.push(current);
            current = current->left;
        }

        // 2. Извлекаем узел, записываем слово
        current = stack.pop();
        out << current->word << std::endl;

        // 3. Переходим к правому поддереву
        current = current->right;
    }
}

void deleteTree(TreeNode* root) {
    if (!root) return;
    deleteTree(root->left);
    deleteTree(root->right);
    delete root;
}

int main() {
    const std::string inputFile = "treerow.txt";
    const std::string outputFile = "treedone.txt";

    // 1. Чтение слов из файла
    std::ifstream fin(inputFile);
    if (!fin.is_open()) {
        std::cerr << "Ошибка: не удалось открыть файл '" << inputFile << "'\n";
        return 1;
    }

    std::vector<std::string> words;
    std::string temp;
    while (fin >> temp) {
        std::string lower = toLowerChar(temp);
        words.push_back(std::move(lower));
    }
    fin.close();

    if (words.empty()) {
        std::cerr << "Файл пуст или не содержит слов.\n";
        return 1;
    }

    // 2. Сортировка + удаление дубликатов
    std::sort(words.begin(), words.end());
    words.erase(std::unique(words.begin(), words.end()), words.end());

    // 3. Построение сбалансированного BST
    TreeNode* root = buildBalancedBST(words, 0, static_cast<int>(words.size()) - 1);


    // 4. Вывод характеристик и структуры дерева в консоль
    std::cout << "Уникальные слова:\n";
    for (size_t i = 0; i < words.size(); ++i)
        std::cout << "   [" << (i + 1) << "] " << words[i] << " ";
    std::cout << "\n\n";
    std::cout << "Характеристики дерева:\n";
    std::cout << "Количество уникальных узлов: " << words.size() << std::endl;
    std::cout << "Высота дерева: " << getTreeHeight(root) << "\n\n";

    std::cout << "Структура дерева (повёрнута на 90° по часовой стрелке):" << std::endl;
    std::cout << "┌─ правое поддерево (сверху)" << std::endl;
    std::cout << "└─ левое поддерево (снизу)\n\n";
    printTree(root);
    std::cout <<std::endl;

    // 5. Запись в файл в алфавитном порядке
    std::ofstream fout(outputFile);
    if (!fout.is_open()) {
        std::cerr << "Ошибка: не удалось открыть файл '" << outputFile << "'\n";
        deleteTree(root);
        return 1;
    }

    inorderTraversal(root, fout);
    fout.close();

    // 6. Очистка памяти
    deleteTree(root);

    std::cout << "Готово. " << words.size() << " уникальных слов сохранены в '"<< outputFile << "' в алфавитном порядке." << std::endl;

    return 0;
}
