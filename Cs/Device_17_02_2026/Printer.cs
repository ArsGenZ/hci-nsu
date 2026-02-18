using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Device_17_02_2026
{
    internal class Printer : Device
    {
        public bool IsColor { get; set; }

        public Printer(string name, bool isColor) : base(name)
        {
            IsColor = isColor;
        }

        public override void GetDeviceInfo()
        {
            base.GetDeviceInfo();
            Console.WriteLine($"Тип: Принтер");
            Console.WriteLine($"Цветная печать: {(IsColor ? "Да" : "Нет")}");
            Console.WriteLine();
        }

        protected override bool DoConnect()
        {
            Console.WriteLine("  -> Проверка наличия чернил и бумаги...");
            return true;
        }

        protected override bool DoDisconnect()
        {
            Console.WriteLine("  -> Очистка печатающей головки...");
            return true;
        }
    }
}
