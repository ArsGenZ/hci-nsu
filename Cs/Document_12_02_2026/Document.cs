using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Document_12_02_2026
{
    internal class Document
    {
        public string Title { get; set; }
        public DateTime DateCreated { get; set; }

        public Document(string title, DateTime dateCreated)
        {
            Title = title;
            DateCreated = dateCreated;
        }

        // Виртуальный метод Print
        public virtual void Print()
        {
            Console.WriteLine($"--- Документ ---");
            Console.WriteLine($"Заголовок: {Title}");
            Console.WriteLine($"Дата создания: {DateCreated.ToShortDateString()}");
        }
    }
}
