using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Document_12_02_2026
{
    internal class SpreadsheetDocument : Document
    {
        public int CellCount { get; set; }

        public SpreadsheetDocument(string title, DateTime date, int cellCount)
            : base(title, date)
        {
            CellCount = cellCount;
        }

        public override void Print()
        {
            base.Print();
            Console.WriteLine($"Тип: Электронная таблица");
            Console.WriteLine($"Количество ячеек: {CellCount}");
            Console.WriteLine();
        }
    }
}
