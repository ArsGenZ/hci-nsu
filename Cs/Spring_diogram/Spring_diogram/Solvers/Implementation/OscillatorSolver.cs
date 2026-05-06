using Spring_diogram.DATA;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Spring_diogram.Solvers.Implementation
{
    public class OscillatorSolver : IEquasionSolver
    {
        public SolverResult Solve(InputData input)
        {
            if (input is not OscillatorInput osc)
                throw new ArgumentException("Неверный тип данных для OscillatorSolver");

            var result = SolverMethods.OscillatorSolve(
                osc.Mass, osc.Stiffness, osc.Damping,
                osc.X0, osc.V0, osc.MaxTime, osc.DeltaT);

            return new SolverResult
            {
                XValues = result[0],
                YValues = result[1],
                Title = "Колебания осциллятора"
            };
        }
    }
}
