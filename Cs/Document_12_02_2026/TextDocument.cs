using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Document_12_02_2026
{
    internal class TextDocument : Document
    {
        public string Content { get; set; }

        public TextDocument(string title, DateTime date, string content)
            : base(title, date)
        {
            Content = content;
        }

        public override void Print()
        {
            base.Print();
            Console.WriteLine($"Тип: Текстовый документ");
            Console.WriteLine($"Содержание: {Content}");
            Console.WriteLine();
        }
    }
}
