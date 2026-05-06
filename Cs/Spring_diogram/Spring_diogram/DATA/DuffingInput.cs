using Spring_diogram.Solvers;

namespace Spring_diogram.DATA
{
    public class DuffingInput : InputData
    {
        public double Delta { get; set; } // Коэффициент затухания
        public double Alpha { get; set; } // Линейная жёсткость (отрицательная = двухъямный потенциал)
        public double Beta { get; set; } // Нелинейная жёсткость
        public double Gamma { get; set; } // Амплитуда вынуждающей силы
        public double Omega { get; set; } // Частота вынуждающей силы
        public double X0 { get; set; } // Начальная координата
        public double V0 { get; set; } // Начальная скорость
        public double SkipTransient { get; set; } // Время "прогрева" до записи данных
        public int RecordStride { get; set; } // Записывать каждую N-ю точку

        public override IEquasionSolver GetSolver()
        {
            return new Solvers.Implementation.DuffingSolver();
        }

        public override string ToString()
        {
            return $"Тип: Нелинейный осциллятор Дуффинга\n" +
                   $"Затухание (Delta): {Delta}\n" +
                   $"Линейная жёсткость (Alpha): {Alpha}\n" +
                   $"Нелинейная жёсткость (Beta): {Beta}\n" +
                   $"Амплитуда вынуждающей силы (Gamma): {Gamma}\n" +
                   $"Частота вынуждающей силы (Omega): {Omega}\n" +
                   $"Начальная координата (X0): {X0}\n" +
                   $"Начальная скорость (V0): {V0}\n" +
                   $"Время прогрева: {SkipTransient} с\n" +
                   $"Шаг записи: {RecordStride}\n" +
                   $"Время: {MaxTime} с\n" +
                   $"Шаг: {DeltaT} с";
        }
    }
}
