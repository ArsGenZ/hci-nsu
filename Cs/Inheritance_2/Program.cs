namespace Inheritance_2
{
    internal class Program
    {
        static void Main(string[] args)
        {
            Shape rectangle = new Rectangle(10,10);
            rectangle.PrintInfo();
            Shape circle = new Circle(10);
            circle.PrintInfo();
            Shape triangle = new Triangle(5, 5, 5);
            triangle.PrintInfo();

            Shape[] shapes = {rectangle, circle, triangle};
            foreach (Shape shape in shapes)
            {
                shape.PrintInfo();
                if (shape is Circle c)
                {
                    Console.WriteLine(c.Radius);
                }
            }
        }
    }
}
