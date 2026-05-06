using Spring_diogram.DATA;

namespace Spring_diogram.Solvers
{
    public interface IEquasionSolver
    {
        SolverResult Solve(InputData input);
    }
}
