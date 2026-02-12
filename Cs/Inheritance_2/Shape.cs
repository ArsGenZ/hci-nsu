using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Inheritance_2
{
    internal abstract class Shape
    {
        public abstract double Area {  get; }
        public abstract double Perimeter { get; }

        public void PrintInfo()
        {
            Console.WriteLine($"Area =: {Area} and Perimetr =: {Perimeter}");
        }
    }
}
