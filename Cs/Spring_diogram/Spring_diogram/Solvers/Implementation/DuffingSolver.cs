using Spring_diogram.DATA;
using System;
using System.Collections.Generic;
using System.Linq;

namespace Spring_diogram.Solvers.Implementation
{
    public class DuffingSolver : IEquasionSolver
    {
        public SolverResult Solve(InputData input)
        {
            if (input is not DuffingInput duffing)
                throw new ArgumentException("Неверный тип данных для DuffingSolver");

            try
            {
                var trajectory = DuffingOscillatorSolver.Solve(duffing);

                // Преобразуем PhasePoint в массивы для графика (Position -> X, Velocity -> Y)
                var positions = trajectory.Select(p => p.Position).ToArray();
                var velocities = trajectory.Select(p => p.Velocity).ToArray();

                return new SolverResult
                {
                    XValues = positions,
                    YValues = velocities,
                    Title = "Фазовая траектория осциллятора Дуффинга"
                };
            }
            catch (ArithmeticException ex)
            {
                throw new ArithmeticException($"Ошибка при расчете задачи Дуффинга: {ex.Message}", ex);
            }
        }
    }
}
