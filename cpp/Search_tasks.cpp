#include <iostream>
#include <cmath>
#include <string>
#include <algorithm>

void createarr(int* arr, int n)
{
    for (int i = 0; i < n; i++)
        std::cin >> arr[i];
}

void createarr2(double* arr, int n)
{
    for (int i = 0; i < n; i++)
        std::cin >> arr[i];
}

int bin_search(int* arr, int n, int x)
{
    int left = 0, right = n - 1, mid;
    while (left <= right) {
        mid = (left + right) / 2;
        if (arr[mid] == x)
            return mid;
        if (arr[mid] < x)
            left = mid + 1;
        else
            right = mid - 1;
    }
    return -1;
}

int bin_search2(double* arr, int n, double x)
{
    int left = 0, right = n - 1, mid;
    while (left <= right) {
        mid = (left + right) / 2;
        if (arr[mid] == x)
            return mid;
        if (arr[mid] < x)
            left = mid + 1;
        else
            right = mid - 1;
    }
    if (abs(x - arr[left]) < abs(x - arr[right]))
        return left;
    else
        return right;
}

int BoyerMooreSearchAll(std::string str, std::string search_str, int* index)
{
    int n = str.size();
    int m = search_str.size();

    if (n == 0 || m > n || m == 0)
        return -1;

    int badChar[256];
        for (int i = 0; i < 256; i++)
            badChar[i] = m;
        for (int i = 0; i < m - 1; i++)
            badChar[search_str[i]] = m - i - 1;

        int count = 0;
        int s = 0;

        while (s <= n - m)
        {
            int j = m - 1;
            while (j >= 0 && search_str[j] == str[s + j])
                j--;

            if (j < 0)
            {
                index[count] = s;
                count++;
                s += (s + m < n) ? badChar[str[s + m]] : 1;
            } else
            {
                int shift = badChar[str[s + m - 1]];
                s += std::max(1, shift);
            }
        }
    return count;
}

int bin_search3(int a[], int l, int r, int x) {
    int result = -1;
    while (l <= r) {
        int mid = (l + r) / 2;
        if (a[mid] == x) {
            result = mid;
            l = mid + 1;
        } else if (a[mid] < x) {
            l = mid + 1;
        } else {
            r = mid - 1;
        }
    }
    return result;
}

int main()
{
    //task 1
    // int size, num;
    // std::cout<<"Enter size of array and number to search: ";
    // std::cin >> size >> num;
    // int* arr = new int[size];
    // createarr(arr, size);
    // int result =bin_search(arr, size, num);
    // delete[] arr;
    // std::cout << "Number found at index: " << result << std::endl;
    //return 0;

    //task 2
    // int size; double num;
    // std::cout<<"Enter size of array and number to search: ";
    // std::cin >> size >> num;
    // double* arr = new double[size];
    // createarr2(arr, size);
    // int result = bin_search2(arr, size, num);
    // delete[] arr;
    // std::cout << "Number found at index: " << result << std::endl;
    // return 0;

    //task 3
   std::string* str = new std::string();
   std::string* search_str = new std::string();
   std::cout << "Enter string to search in: ";
   std::cin >> *str;
   std::cout << "Enter string to search: ";
   std::cin >> *search_str;
   int* index = new int(str->size());
   int count = 0;
   count = BoyerMooreSearchAll(*str, *search_str, index);
   std::cout << count << std::endl;
   for (int i = 0; i < count; i++)
   {
       std::cout << index[i] << std::endl;
   }
   free(str);
   free(search_str);
   return 0;
   /*
    * aaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
    * HELP ME! HELP ME! HELP ME!
    * HELP ME! HELP ME! HELP ME!
    * HELP ME! HELP ME! HELP ME!
    * HELP ME! HELP ME! HELP ME!
    * HELP ME! HELP ME! HELP ME!
    * HELP ME! HELP ME! HELP ME!
    * HELP ME! HELP ME! HELP ME!
    * aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
    */

   //task 4
//    int size;
//    std::cout<<"Enter size of array: ";
//    std::cin >> size;
//    int* arr = new int[size];
//    createarr(arr, size);

//    int q;
//    std::cout << "Enter number of queries: ";
//    std::cin >> q;

//    int prev_anaswer = 0;
//    for (int i = 0; i < q; i++)
//    {
//        int x;
//        std::cin >> x;
//        x += prev_anaswer;
//        int result = bin_search3(arr, 0, size - 1, x);
//        std::cout << result << std::endl;
//        prev_anaswer = result;
//    }
//    delete[] arr;
//    return 0;
}
