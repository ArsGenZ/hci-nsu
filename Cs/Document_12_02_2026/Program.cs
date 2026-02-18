namespace Document_12_02_2026
{
    internal class Program
    {
        static void Main(string[] args)
        {
            Document[] docs = new Document[3];

            docs[0] = new TextDocument("Отчет за год", DateTime.Now, "Текст отчета...");
            docs[1] = new SpreadsheetDocument("Бюджет 2024", DateTime.Now.AddDays(-5), 1500);
            docs[2] = new PresentationDocument("План развития", DateTime.Now.AddDays(-10), 25);

            DocumentManager.PrintAll(docs);
        }
    }
}
