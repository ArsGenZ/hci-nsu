using OxyPlot;
using Spring_diogram.Common;
using Spring_diogram.Solvers;
using System.Windows.Input;
using System.Windows;

namespace Spring_diogram.ViewModel
{
    public class SolverViewModel : ViewModelBase
    {
        private readonly UndoRedoManager _undoRedoManager;
        private readonly InputViewModel _inputViewModel;
        private PlotModel? _plotModel;
        private SolverResult? _solverResult;

        public SolverViewModel(UndoRedoManager undoRedoManager, InputViewModel inputViewModel)
        {
            _undoRedoManager = undoRedoManager;
            _inputViewModel = inputViewModel;
            SolveCommand = new RelayCommand(_ => Solve(), CanSolve);
        }

        public ICommand SolveCommand { get; }

        private bool CanSolve(object parameter)
        {
            return _inputViewModel.CurrentImportedData != null;
        }

        public PlotModel? PlotModel
        {
            get => _plotModel;
            set
            {
                if (_plotModel != value)
                {
                    var oldValue = _plotModel;
                    _plotModel = value;
                    OnPropertyChanged();
                    _undoRedoManager.AddUndoRedo(
                        () => { _plotModel = oldValue; OnPropertyChanged(nameof(PlotModel)); },
                        () => { _plotModel = value; OnPropertyChanged(nameof(PlotModel)); }
                    );
                }
            }
        }

        public SolverResult? SolverResult
        {
            get => _solverResult;
            set
            {
                if (_solverResult != value)
                {
                    var oldValue = _solverResult;
                    _solverResult = value;
                    OnPropertyChanged();
                    _undoRedoManager.AddUndoRedo(
                        () => { _solverResult = oldValue; OnPropertyChanged(nameof(SolverResult)); },
                        () => { _solverResult = value; OnPropertyChanged(nameof(SolverResult)); }
                    );
                }
            }
        }

        public void Solve()
        {
            var inputData = _inputViewModel.CurrentImportedData;
            if (inputData == null)
                throw new System.Exception("Входные данные не загружены!");

            try
            {
                var solver = inputData.GetSolver();
                var result = solver.Solve(inputData);
                SolverResult = result;
                PlotModel = CreatePlotModel(result);
            }
            catch (ArithmeticException ex)
            {
                MessageBox.Show($"Ошибка при расчете задачи: {ex.Message}", "Ошибка вычисления", MessageBoxButton.OK, MessageBoxImage.Error);
            }
        }

        private PlotModel CreatePlotModel(SolverResult result)
        {
            var plotModel = new PlotModel { Title = result.Title };
            var series = new OxyPlot.Series.LineSeries();

            int minLength = System.Math.Min(result.XValues.Length, result.YValues.Length);
            for (int i = 0; i < minLength; i++)
            {
                series.Points.Add(new OxyPlot.DataPoint(result.XValues[i], result.YValues[i]));
            }

            plotModel.Series.Add(series);
            return plotModel;
        }
    }
}
