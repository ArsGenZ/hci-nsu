namespace Spring_diogram.Solvers.Implementation
{
    public static class SolverMethods
    {
        public static double[][] OscillatorSolve(double m, double stiffness,
            double damping, double x0, double v0, double tMax, double dt)
        {
            int n = 0;
            n = (int)(tMax / dt) + 1;
            double[] t = new double[n];
            double[] x = new double[n];
            double[] v = new double[n];

            t[0] = 0; x[0] = x0; v[0] = v0;

            for (int i = 0; i < n - 1; i++)
            {
                double ti = t[i];
                double xi = x[i];
                double vi = v[i];

                double k1x = vi;
                double k1v = -(damping / m) * vi - (stiffness / m) * xi;

                double k2x = vi + k1v * dt / 2;
                double k2v = -(damping / m) * (vi + k1v * dt / 2) - (stiffness / m) * (xi + k1x * dt / 2);

                double k3x = vi + k2v * dt / 2;
                double k3v = -(damping / m) * (vi + k2v * dt / 2) - (stiffness / m) * (xi + k2x * dt / 2);

                double k4x = vi + k3v * dt;
                double k4v = -(damping / m) * (vi + k3v * dt) - (stiffness / m) * (xi + k3x * dt);

                x[i + 1] = xi + (k1x + 2 * k2x + 2 * k3x + k4x) * dt / 6;
                v[i + 1] = vi + (k1v + 2 * k2v + 2 * k3v + k4v) * dt / 6;
                t[i + 1] = ti + dt;
            }
            return new[] { t, x };
        }

        public static double[][] RcSolve(double r, double c, double voltageSource, double u0, double tMax, double dt)
        {
            return Solve((time, u) => (voltageSource - u) / (r * c), u0, 0, tMax, dt);
        }

        public static double[][] CoolingSolve(double c, double tEnv, double t0, double tMax, double dt)
        {
            return Solve((t, temp) => -c * (temp - tEnv), t0, 0, tMax, dt);
        }

        private static double[][] Solve(Func<double, double, double> f, double y0, double t0, double tMax, double dt)
        {
            int steps = (int)((tMax - t0) / dt) + 1;
            double[] t = new double[steps];
            double[] y = new double[steps];

            t[0] = t0;
            y[0] = y0;

            for (int i = 0; i < steps - 1; i++)
            {
                double ti = t[i];
                double yi = y[i];

                double k1 = f(ti, yi);
                double k2 = f(ti + dt / 2, yi + k1 * dt / 2);
                double k3 = f(ti + dt / 2, yi + k2 * dt / 2);
                double k4 = f(ti + dt, yi + k3 * dt);

                y[i + 1] = yi + (k1 + 2 * k2 + 2 * k3 + k4) * dt / 6;
                t[i + 1] = ti + dt;
            }
            return new[] { t, y };
        }
    }
}
