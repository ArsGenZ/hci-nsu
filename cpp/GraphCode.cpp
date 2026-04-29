#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <stdexcept>
#include <iomanip>

using namespace std;

// Функция для вывода текущего состояния матрицы
void printState(const vector<vector<int>>& adj, int n, int iter, int chosenV, const vector<int>& result) {
    cout << "\n--- Шаг " << iter << " ---\n";
    if (chosenV != -1) {
        cout << "[INFO] Найдена вершина с нулевым входящим потоком: " << chosenV << "\n";
    }
    cout << "[ORDER] Топологический порядок: ";
    if (result.empty())
        cout << "(пусто)";
    else {
        for (size_t i = 0; i < result.size(); ++i) {
            cout << result[i] << (i == result.size() - 1 ? "" : " -> ");
        }
    }
    cout << "\n";

    cout << "[MATRIX] Матрица смежности:\n";
    cout << "     ";
    for (int j = 0; j < n; ++j) {
        cout << setw(4) << j;
    }
    cout << "\n";
    for (int i = 0; i < n; ++i) {
        cout << "  " << i << ":";
        for (int j = 0; j < n; ++j)
            cout << setw(4) << adj[i][j];
        cout << "\n";
    }
    cout << "--------------------------\n";
}

// 1. чтение файла
vector<vector<int>> readAdjacencyMatrix(const string& filename, int& n) {
    ifstream file(filename);
    if (!file.is_open()) {
        throw runtime_error("Не удалось открыть файл: " + filename);
    }

    file >> n;
    if (n <= 0) throw runtime_error("Некорректное количество вершин (должно быть > 0)");

    vector<vector<int>> matrix(n, vector<int>(n));
    for (int i = 0; i < n; ++i) {
        for (int j = 0; j < n; ++j) {
            file >> matrix[i][j];
        }
    }
    return matrix;
}

// 2. Реализовать алгоритм топологической сортировки на матрице смежности
vector<int> topologicalSort(vector<vector<int>> adj, int n) {
    vector<int> result;
    vector<bool> processed(n, false);
    int processedCount = 0;
    int iteration = 0;


    // 4. шаг Пока не перебрали все вершины, повторять шаг 1.
    while (processedCount < n) {
        printState(adj, n, iteration, -1, result);
        iteration++;
        int v = -1;

        // 1 шаг. Найти вершину, в которую не входит ни одна дуга.
        for (int j = 0; j < n; ++j) {
            if (processed[j]) continue;

            bool hasIncoming = false;
            for (int i = 0; i < n; ++i) {
                if (adj[i][j] != 0) {
                    hasIncoming = true;
                    break;
                }
            }

            if (!hasIncoming) {
                v = j;
                break;
            }
        }

        if (v == -1) {
            cout << "\n[ERROR] Не найдена вершина с нулевым входящим потоком.\n";
            throw runtime_error("Граф содержит цикл. Топологическая сортировка невозможна.");
        }

        // 2 шаг. Записать вершину в результат и пометить как пройденную.
        result.push_back(v);
        processed[v] = true;

        // 3 шаг. Удалить все выходящие дуги: обнулить строку.
        for (int j = 0; j < n; ++j) {
            adj[v][j] = 0;
        }

        // Вывод состояния после выполнения шагов 2 и 3
        printState(adj, n, iteration, v, result);

        processedCount++;
    }

    return result;
}

int main() {
    try {
        string filename = "graph.txt";
        int n;

        cout << "[INFO] Чтение файла: " << filename << "...\n";
        vector<vector<int>> matrix = readAdjacencyMatrix(filename, n);
        cout << "[OK] Матрица успешно загружена (" << n << " вершин).\n";

        vector<int> topoOrder = topologicalSort(matrix, n);

        cout << "\n[RESULT] Итоговый результат топологической сортировки:\n";
        for (int v : topoOrder) {
            cout << v << " ";
        }
        cout << "\n";
    } catch (const exception& e) {
        cerr << "\n[ERROR] " << e.what() << "\n";
        return 1;
    }
    return 0;
}
