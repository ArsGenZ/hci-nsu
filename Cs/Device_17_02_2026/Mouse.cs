using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Device_17_02_2026
{
    internal class Mouse : Device
    {
        public int Dpi { get; set; }

        public Mouse(string name, int dpi) : base(name)
        {
            Dpi = dpi;
        }

        public override void GetDeviceInfo()
        {
            base.GetDeviceInfo();
            Console.WriteLine($"Тип: Мышь");
            Console.WriteLine($"Разрешение (DPI): {Dpi}");
            Console.WriteLine();
        }

        protected override bool DoConnect()
        {
            Console.WriteLine("  -> Калибровка сенсора мыши...");
            return true;
        }

        protected override bool DoDisconnect()
        {
            Console.WriteLine("  -> Остановка сенсора мыши...");
            return true;
        }
    }
}
