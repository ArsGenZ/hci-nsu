using Spring_diogram.DATA;

namespace Spring_diogram.Solvers.Implementation
{
    public class CoolingSolver : IEquasionSolver
    {
        public SolverResult Solve(InputData input)
        {
            if (input is not CoolingInput cool)
                throw new ArgumentException("Неверный тип данных для CoolingSolver");

            var result = SolverMethods.CoolingSolve(
                cool.Coeff, cool.Tenv, cool.T0,
                cool.MaxTime, cool.DeltaT);

            return new SolverResult
            {
                XValues = result[0],
                YValues = result[1],
                Title = "Охлаждение тела"
            };
        }
    }
}
