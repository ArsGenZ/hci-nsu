using Spring_diogram.Solvers;

namespace Spring_diogram.DATA
{
    public class CoolingInput : InputData
    {
        public double T0 { get; set; }
        public double Tenv { get; set; }
        public double Coeff { get; set; }

        public override IEquasionSolver GetSolver()
        {
            return new Solvers.Implementation.CoolingSolver();
        }

        public override string ToString()
        {
            return $"Тип: Охлаждение\n" +
                   $"Начальная температура: {T0} °C\n" +
                   $"Температура среды: {Tenv} °C\n" +
                   $"Коэффициент: {Coeff} 1/с\n" +
                   $"Время: {MaxTime} с\n" +
                   $"Шаг: {DeltaT} с";
        }
    }
}
