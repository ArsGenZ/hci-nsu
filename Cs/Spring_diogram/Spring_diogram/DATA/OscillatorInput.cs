using Spring_diogram.Solvers;
using Spring_diogram.Solvers.Implementation;

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
            return new OscillatorSolver();
        }
    }
}
