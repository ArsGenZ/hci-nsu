using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Inheritance_2
{
    internal class Triangle : Shape
    {
        public double SideA { get; }
        public double SideB { get; }
        public double SideC { get; }

        public Triangle(double a, double b, double c)
        {
            if (a <= 0 || b <= 0 || c <= 0)
                Console.WriteLine("Стороны должны быть положительными!");
            else
            {

                if (a + b <= c || a + c <= b || b + c <= a)
                    Console.WriteLine("Треугольник с такими сторонами не существует");
                else
                {
                    SideA = a;
                    SideB = b;
                    SideC = c;
                }
            }
        }

        public override double Area
        {
            get
            {
                double p = Perimeter / 2;
                return Math.Sqrt(p * (p - SideA) * (p - SideB) * (p - SideC));
            }
        }

        public override double Perimeter => SideA + SideB + SideC;
    }
}

