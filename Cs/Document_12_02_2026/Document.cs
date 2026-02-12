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
        public string DateCreated { get; set; }

        internal Document(string Title, string DateCreated)
        {

        }
        protected virtual void Print()
        {
            Console.WriteLine($"Title - {Title}");
            Console.WriteLine($"Created date - {DateCreated}");
        }
    }
}
