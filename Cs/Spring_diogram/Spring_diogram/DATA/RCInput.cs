using Spring_diogram.Solvers;

namespace Spring_diogram.DATA
{
    public class RCInput : InputData
    {
        public double Resistance { get; set; }
        public double Capacitance { get; set; }
        public double VoltageSource { get; set; }
        public double U0 { get; set; }

        public override IEquasionSolver GetSolver()
        {
            return new Solvers.Implementation.RcSolver();
        }

        public override string ToString()
        {
            return $"Тип: RC Цепь\n" +
                   $"Сопротивление: {Resistance} Ом\n" +
                   $"Ёмкость: {Capacitance} Ф\n" +
                   $"Напряжение источника: {VoltageSource} В\n" +
                   $"Начальное напряжение: {U0} В\n" +
                   $"Время: {MaxTime} с\n" +
                   $"Шаг: {DeltaT} с";
        }
    }
}
