#include <iostream>

bool is_prime(int num)
{
    for (int i = 2; i*i <= (num); i++)
    {
        if (num % i == 0)
            return false;
    }
    return true;
}

void create_mass(int* mas, int num)
{
    mas[0] = 2;
    mas[1] = 3;
    for (int i = 2; i < num; i++)
    {
        mas[i] = i + 2;
    }
}

void print_mass(int* mas, int num)
{
    for (int i = 0; i < num; i++)
    {
        std:: cout << mas[i] << " ";
    }
    std:: cout << std::endl;
}

void mass_srez(int* mas, int index, int num)
{
    for (int i = num; i > index; i--)
    {

    }
}


int main()
{
    // //task1
    // int num;
    // std:: cout<<"Введите число" << std::endl;
    // std:: cin >> num;
    // if (is_prime(num) == false  || num == 1)
    //     std:: cout << "NO" << std::endl;
    // else
    //     std:: cout << "YES" << std::endl;

    // //task2
    // int num;
    // std:: cout<<"Введите число" << std::endl;
    // std:: cin >> num;
    // for (int i = 2; i <= num; i++)
    // {
    //     if (is_prime(i) == true)
    //         std:: cout << i << " ";
    // }
    // std:: cout << std::endl;

    // //task3
    // int N;
    // std::cout << "Введите натуральное число N: ";
    // std::cin >> N;

    // if (N < 2)
    // {
    //     std::cout << "Нет простых чисел, не превосходящих " << N << std::endl;
    //     return 0;
    // }

    //     std::vector<bool> isPrime(N + 1, true);
    //     isPrime[0] = false;
    //     isPrime[1] = false;

    //     for (int K = 2; K * K <= N; K++)
    //     {
    //         if (isPrime[K])
    //         {
    //             for (int j = K * K; j <= N; j += K)
    //             {
    //                 isPrime[j] = false;
    //             }
    //         }
    //     }

    // std::cout << "Простые числа, не превосходящие " << N << ":\n";
    // for (int i = 2; i <= N; i++) {
    //     if (isPrime[i])
    //     {
    //         std::cout << i << " ";
    //     }
    // }
    // std::cout << std::endl;

    // //task4
    int N, K, count;
    std:: cin >> N >> K;

    for (int i = 0; i < K; i++)
    {
        std:: cin >> count;
        if (count > N || count < 0)
        {
            std:: cout << "Число не находится в диапозоне, введите число ещё раз" << std::endl;
            i--;
        }
        else
        {
            if (is_prime(count) && count != 1 && count != 0)
                std:: cout << "\t" << count << " prime" << std::endl;
            else
                std:: cout << "\t" << count << " not" << std::endl;
        }
    }

    return 0;
}
