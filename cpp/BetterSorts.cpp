#include <iostream>
#include <algorithm>

void heapify(int arr[], int size, int root);

void createArray(int arr[], int size) {
    for (int i = 0; i < size; i++) {
        std::cin >> arr[i];
    }
    std::cout << std::endl;
}

void printArray(int arr[], int size) {
    for (int i = 0; i < size; i++) {
        std::cout << arr[i] << " ";
    }
    std::cout << std::endl;
}

void ShellSort(int arr[], int size) {
    int gap = size / 2;
    while (gap > 0) {
        for (int i = gap; i < size; i++) {
            int temp = arr[i];
            int j = i;
            while (j >= gap && arr[j - gap] > temp) {
                arr[j] = arr[j - gap];
                j -= gap;
            }
            arr[j] = temp;
        }
        gap /= 2;
    }
}

// Pyramid Sort!!!!
// **********************************************************************
void HeapSort(int arr[], int n) {
    for (int i = n / 2 - 1; i >= 0; i--)
        heapify(arr, n, i);

    for (int i=n-1; i>=0; i--)
    {
        std::swap(arr[0], arr[i]);

        heapify(arr, i, 0);
    }
}

void heapify(int arr[], int size, int root) {
    int largest = root;
    int left = 2 * root + 1;
    int right = 2 * root + 2;

    if (left < size && arr[left] > arr[largest]) {
        largest = left;
    }
    if (right < size && arr[right] > arr[largest]) {
        largest = right;
    }
    if (largest != root) {
        std::swap(arr[root], arr[largest]);
        heapify(arr, size, largest);
    }
}
//********************************************************

// Fast Sort
void FastSort(int arr[], int size) {
    if (size <= 1) return;

    int pivot = arr[size / 2];
    int l = -1, r = size;

    while (true) {
        do ++l; while (arr[l] < pivot);
        do --r; while (arr[r] > pivot);
        if (l >= r) break;
        std::swap(arr[l], arr[r]);
    }

    FastSort(arr, l);
    FastSort(arr + l, size - l);
}

int main() {
    //Shell
    int n;
    std::cin >> n;
    int* arr = new int[n];
    createArray(arr, n);
    ShellSort(arr, n);
    printArray(arr, n);
    return 0;

    //Pyramid
    // int n;
    // std::cin >> n;
    // int* arr = new int[n];
    // createArray(arr, n);
    // HeapSort(arr, n);
    // printArray(arr, n);
    // return 0;

    //FastSort
    // int n;
    // std::cin >> n;
    // int* arr = new int[n];
    // createArray(arr, n);
    // FastSort(arr, n);
    // printArray(arr, n);
    // return 0;
}
