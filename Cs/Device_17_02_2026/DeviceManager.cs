using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Device_17_02_2026
{
    internal class DeviceManager
    {
        public static void PrintAllDevices(Device[] devices)
        {
            Console.WriteLine("=== Информация обо всех устройствах ===\n");

            foreach (var device in devices)
            {
                device.GetDeviceInfo();
            }
        }
    }
}
