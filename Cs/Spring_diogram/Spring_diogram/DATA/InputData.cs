using Spring_diogram.Solvers;

namespace Spring_diogram.DATA
{
    public abstract class InputData
    {
        public string Name { get; set; } = "";
        public double MaxTime { get; set; }
        public double DeltaT { get; set; }

        public abstract IEquasionSolver GetSolver();

        public override string ToString()
        {
            return Name;
        }
    }
}
