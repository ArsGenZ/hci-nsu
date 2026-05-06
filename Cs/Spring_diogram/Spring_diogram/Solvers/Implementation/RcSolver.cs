using Spring_diogram.DATA;

namespace Spring_diogram.Solvers.Implementation
{
    public class RcSolver : IEquasionSolver
    {
        public SolverResult Solve(InputData input)
        {
            if (input is not RCInput rc)
                throw new ArgumentException("Неверный тип данных для RcSolver");

            var result = SolverMethods.RcSolve(
                rc.Resistance, rc.Capacitance, rc.VoltageSource,
                rc.U0, rc.MaxTime, rc.DeltaT);

            return new SolverResult
            {
                XValues = result[0],
                YValues = result[1],
                Title = "Заряд конденсатора (RC)"
            };
        }
    }
}
