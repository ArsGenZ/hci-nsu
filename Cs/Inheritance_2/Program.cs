namespace Inheritance_2
{
    internal class Program
    {
        static void Main(string[] args)
        {
            Rectangle rectangle = new Rectangle(10,10);rectangle.PrintInfo();
            Circle circle = new Circle(10);circle.PrintInfo();
            Triangle triangle = new Triangle(5, 5, 5);triangle.PrintInfo();
        }
    }
}
