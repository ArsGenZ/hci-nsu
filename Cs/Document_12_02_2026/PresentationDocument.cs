using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Document_12_02_2026
{
    internal class PresentationDocument : Document
    {
        public int SlideCount { get; set; }

        public PresentationDocument(string title, DateTime date, int slideCount)
            : base(title, date)
        {
            SlideCount = slideCount;
        }

        public override void Print()
        {
            base.Print();
            Console.WriteLine($"Тип: Презентация");
            Console.WriteLine($"Количество слайдов: {SlideCount}");
            Console.WriteLine();
        }
    }
}
