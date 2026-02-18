using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Document_12_02_2026
{
    internal class DocumentManager
    {
        public static void PrintAll(Document[] documents)
        {
            Console.WriteLine("=== Печать всех документов ===\n");

            foreach (var doc in documents)
            {
                doc.Print();
            }
        }
    }
}
