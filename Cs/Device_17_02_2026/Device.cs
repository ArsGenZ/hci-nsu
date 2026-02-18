using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Device_17_02_2026
{
    internal abstract class Device
    {
        public string Name { get; set; }

        public virtual bool IsConnected { get; protected set; }

        public Device(string name)
        {
            Name = name;
            IsConnected = false;
        }

        public virtual void GetDeviceInfo()
        {
            Console.WriteLine($"Устройство: {Name}");
            Console.WriteLine($"Статус подключения: {(IsConnected ? "Подключено" : "Отключено")}");
        }

        public void Connect()
        {
            Console.WriteLine($"Попытка подключения: {Name}...");

            if (DoConnect())
            {
                IsConnected = true;
                Console.WriteLine($"Устройство {Name} успешно подключено.\n");
            }
            else
            {
                Console.WriteLine($"Не удалось подключить устройство {Name}.\n");
            }
        }

        public void Disconnect()
        {
            Console.WriteLine($"Попытка отключения: {Name}...");

            if (DoDisconnect())
            {
                IsConnected = false;
                Console.WriteLine($"Устройство {Name} успешно отключено.\n");
            }
            else
            {
                Console.WriteLine($"Не удалось отключить устройство {Name}.\n");
            }
        }

        protected abstract bool DoConnect();

        protected abstract bool DoDisconnect();
    }
}
