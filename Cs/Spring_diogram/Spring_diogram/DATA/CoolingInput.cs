using Spring_diogram.Solvers;
using Spring_diogram.Solvers.Implementation;

namespace Spring_diogram.DATA
{
    public class CoolingInput : InputData
    {
        public double T0 { get; set; }
        public double Tenv { get; set; }
        public double Coeff { get; set; }

        public override IEquasionSolver GetSolver()
        {
            return new CoolingSolver();
        }
    }
}
