namespace Device_17_02_2026
{
    internal class Program
    {
        static void Main(string[] args)
        {
            Device[] devices = new Device[3];

            devices[0] = new Keyboard("Logitech K120", 104);
            devices[1] = new Mouse("Razer DeathAdder", 16000);
            devices[2] = new Printer("HP LaserJet", true);

            Console.WriteLine(">>> Состояние до подключения:\n");
            DeviceManager.PrintAllDevices(devices);

            Console.WriteLine(">>> Подключение устройств:\n");
            foreach (var device in devices)
            {
                device.Connect();
            }

            Console.WriteLine(">>> Состояние после подключения:\n");
            DeviceManager.PrintAllDevices(devices);

            Console.WriteLine(">>> Отключение клавиатуры:\n");
            devices[0].Disconnect();

            Console.WriteLine(">>> Финальное состояние:\n");
            DeviceManager.PrintAllDevices(devices);

            var mouse_devices = devices.OfType<Mouse>().ToArray();
            foreach(var mouse in mouse_devices)
            {
                if (mouse.Name == "Razer DeathAdder")
                    Console.WriteLine("YYYYYYYYYYYYYYYYAAAAAAAAAAAAAAAAAAAA");
            }
        }
    }
}
