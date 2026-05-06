namespace Spring_diogram.Solvers.Implementation
{
    public struct PhasePoint
    {
        public double Position { get; set; }
        public double Velocity { get; set; }

        public PhasePoint(double x, double v)
        {
            (Position, Velocity) = (x, v);
        }
    }
}
