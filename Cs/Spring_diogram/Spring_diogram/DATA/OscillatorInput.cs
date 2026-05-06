using Spring_diogram.Solvers;

namespace Spring_diogram.DATA
{
    public class OscillatorInput : InputData
    {
        public double Mass { get; set; }
        public double Stiffness { get; set; }
        public double Damping { get; set; }
        public double X0 { get; set; }
        public double V0 { get; set; }

        public override IEquasionSolver GetSolver()
        {
            return new Solvers.Implementation.OscillatorSolver();
        }

        public override string ToString()
        {
            return $"Тип: Маятник\n" +
                   $"Масса: {Mass} кг\n" +
                   $"Жесткость: {Stiffness} Н/м\n" +
                   $"Затухание: {Damping} кг/с\n" +
                   $"X0: {X0} м\n" +
                   $"V0: {V0} м/с\n" +
                   $"Время: {MaxTime} с\n" +
                   $"Шаг: {DeltaT} с";
        }
    }
}
