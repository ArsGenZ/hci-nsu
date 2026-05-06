using Spring_diogram.Solvers;
using Spring_diogram.Solvers.Implementation;

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
            return new RcSolver();
        }
    }
}
