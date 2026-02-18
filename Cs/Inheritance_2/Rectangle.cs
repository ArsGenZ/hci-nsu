using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Inheritance_2
{
    internal class Rectangle : Shape
    {

        public double _width;
        public double _height;
        public double Width { get => _width; set => _width = _width > 0 ? value : _width; }
        public double Height { get => _height; set => _height = _height > 0 ? value : _width ; }

        public Rectangle(double width, double height)
        {
            _width = width;
            _height = height;
        }

        public override double Area => Width * Height;
        public override double Perimeter => 2 * (Width + Height);
    }
}
