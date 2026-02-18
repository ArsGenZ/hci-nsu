using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Device_17_02_2026
{
    internal class Keyboard : Device
    {
        public int KeyCount { get; set; }

        public Keyboard(string name, int keyCount) : base(name)
        {
            KeyCount = keyCount;
        }

        public override void GetDeviceInfo()
        {
            base.GetDeviceInfo();
            Console.WriteLine($"Тип: Клавиатура");
            Console.WriteLine($"Количество клавиш: {KeyCount}");
            Console.WriteLine();
        }

        protected override bool DoConnect()
        {

            Console.WriteLine("  -> Инициализация драйвера клавиатуры...");
            return true;
        }

        protected override bool DoDisconnect()
        {
            Console.WriteLine("  -> Завершение работы драйвера клавиатуры...");
            return true;
        }
    }
}
