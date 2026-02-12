using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Inheritance_2
{
    internal class Rectangle : Shape
    {
        public double Width { get; }
        public double Height { get; }

        public Rectangle(double width, double height)
        {
            if (width <= 0 || height <= 0)
                Console.WriteLine("Стороны должны быть положительными!");
            else
            {
                Width = width;
                Height = height;
            }

        }

        public override double Area => Width * Height;
        public override double Perimeter => 2 * (Width + Height);
    }
}
