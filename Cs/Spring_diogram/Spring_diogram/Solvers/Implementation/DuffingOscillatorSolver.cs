using Spring_diogram.DATA;
using System;
using System.Collections.Generic;

namespace Spring_diogram.Solvers.Implementation
{
    /// <summary>
    ///     Решатель уравнения Дуффинга конечно-разностным методом
    /// </summary>
    public static class DuffingOscillatorSolver
    {
        private static void ValidateParameters(DuffingInput input)
        {
            if (input.DeltaT <= 0) throw new ArgumentException("Dt must be positive");
            if (input.MaxTime <= 0) throw new ArgumentException("TotalTime must be positive");
            if (input.SkipTransient < 0) throw new ArgumentException("SkipTransient must be non-negative");
            // Условие устойчивости схемы (упрощённое)
            if (input.DeltaT > 2.0 / Math.Sqrt(Math.Abs(input.Alpha) + 3 * input.Beta * 10)) // эвристика
                Console.WriteLine($"⚠ Warning: Dt={input.DeltaT} may be too large for stability");
        }

        /// <summary>
        ///     Запустить расчёт и вернуть фазовую траекторию (velocity vs position)
        /// </summary>
        public static IReadOnlyList<PhasePoint> Solve(DuffingInput input)
        {
            ValidateParameters(input);
            
            var trajectory = new List<PhasePoint>();

            var totalSteps = (int)Math.Ceiling(input.MaxTime / input.DeltaT);
            var skipSteps = (int)Math.Ceiling(input.SkipTransient / input.DeltaT);

            // Инициализация: используем метод Эйлера для первого шага
            var x_prev = input.X0;
            var xcurr = input.X0 + input.V0 * input.DeltaT; // x[1] ≈ x[0] + v[0]*dt

            var t = input.DeltaT;

            // Предвычисление констант схемы для ускорения
            var dt2 = input.DeltaT * input.DeltaT;
            var deltadt2 = input.Delta * input.DeltaT / 2.0;
            var denom = 1.0 + deltadt2;

            for (var i = 1; i < totalSteps; i++, t += input.DeltaT)
            {
                // Вычисляем правую часть уравнения в текущей точке
                var forcing = input.Gamma * Math.Cos(input.Omega * t);
                var nonlinear = input.Alpha * xcurr + input.Beta * xcurr * xcurr * xcurr;

                // Конечно-разностная схема (выведена из центральных разностей)
                var xnext = (2.0 * xcurr
                              + x_prev * (deltadt2 - 1.0)
                              - dt2 * (nonlinear - forcing)) / denom;

                // После "прогрева" записываем точки фазовой траектории
                if (i > skipSteps && i % input.RecordStride == 0)
                {
                    // Скорость через центральную разность
                    var velocity = (xnext - x_prev) / (2.0 * input.DeltaT);
                    trajectory.Add(new PhasePoint(xcurr, velocity));
                }

                // Сдвиг по времени
                x_prev = xcurr;
                xcurr = xnext;
            }

            return trajectory.AsReadOnly();
        }
    }
}
