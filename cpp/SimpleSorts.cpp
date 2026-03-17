#include <iostream>

void print_array(int *arr, int n) {
    for (int i = 0; i < n; i++) {
        std::cout << arr[i] << " ";
    }
    std::cout << std::endl;
}


void fill_array(int *arr, int n) {
    for (int i = 0; i < n; i++) {
        std::cin >> arr[i];
    }
    std::cout << std::endl;
}

void ins_sort(int *arr, int n) {
    for (int i = 1; i < n; i++)
    {
        int x = arr[i];
        int j = i - 1;
        while (j >= 0 && arr[j] >= x)
        {
            arr[j + 1] = arr[j];
            j--;
        }
        arr[j + 1] = x;
    }
}

void select_sort(int *arr, int n) {
    for (int i = 0; i < n - 1; i++) {
        int min_idx = i;
        for (int j = i + 1; j < n; j++) {
            if (arr[j] < arr[min_idx]) {
                min_idx = j;
            }
        }
        std::swap(arr[i], arr[min_idx]);
    }
}

void shake_sort(int *arr, int n) {
    bool F = true;
    int left = 0;
    int right = n - 1;

    while (F) {
        F = false;

        for (int i = left; i < right; i++) {
            if (arr[i] > arr[i + 1]) {
                std::swap(arr[i], arr[i + 1]);
                F = true;
            }
        }

        if (!F) break;

        F = false;
        right--;

        for (int i = right - 1; i >= left; i--) {
            if (arr[i] > arr[i + 1]) {
                std::swap(arr[i], arr[i + 1]);
                F = true;
            }
        }

        left++;
    }
}

int main()
{
    //task 1
    int n;
    std::cout << "Enter n: " << std::endl;
    std::cin >> n;
    int *arr = new int[n];
    fill_array(arr, n);
    ins_sort(arr, n);
    print_array(arr, n);
    delete[] arr;
    return 0;

   //task 2
   // int n;
   // std::cout << "Enter n: " << std::endl;
   // std::cin >> n;
   // int *arr = new int[n];
   // fill_array(arr, n);
   // select_sort(arr, n);
   // print_array(arr, n);
   // delete[] arr;
   // return 0;

   //task 3
   // int n;
   // std::cout << "Enter n: " << std::endl;
   // std::cin >> n;
   // int *arr = new int[n];
   // fill_array(arr, n);
   // shake_sort(arr, n);
   // print_array(arr, n);
   // delete[] arr;
   // return 0;

}
