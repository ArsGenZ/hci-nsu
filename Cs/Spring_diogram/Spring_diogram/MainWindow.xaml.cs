using Microsoft.Win32;
using OxyPlot;
using OxyPlot.Series;
using Spring_diogram.Common;
using Spring_diogram.DATA;
using Spring_diogram.Parsers;
using Spring_diogram.Solvers;
using System.Windows;

namespace Spring_diogram
{
        public partial class MainWindow : Window
        {
            private readonly UndoRedoManager _undoManager = new();
            private InputData? _currentInputData;
            private SolverResult? _currentResult;
            //private string _previousInputText = "";
            //private PlotModel? _previousPlotModel;

            public MainWindow()
            {
                InitializeComponent();
            }

            private void BrowseButton_Click(object sender, RoutedEventArgs e)
            {
                OpenFileDialog openFileDialog = new OpenFileDialog
                {
                    Filter = "Text files|*.txt|All files|*.*",
                    Title = "Выберите файл входных данных"
                };

                if (openFileDialog.ShowDialog() == true)
                {
                    FilePathTextBox.Text = openFileDialog.FileName;
                }
            }

            private void LoadButton_Click(object sender, RoutedEventArgs e)
            {
                try
                {
                    string path = FilePathTextBox.Text;
                    if (string.IsNullOrEmpty(path))
                    {
                        MessageBox.Show("Путь к файлу не указан!", "Ошибка", MessageBoxButton.OK, MessageBoxImage.Warning);
                        return;
                    }

                    // Сохраняем предыдущее состояние для Undo
                    var previousInput = _currentInputData;
                    var previousResult = _currentResult;
                    var previousText = InputDataTextBlock.Text;
                    var previousModel = MainPlotView.Model;

                    // Парсинг файла
                    InputData inputData = ParseFile(path);
                    _currentInputData = inputData;

                    // Получение решателя и выполнение расчета
                    var solver = inputData.GetSolver();
                    _currentResult = solver.Solve(inputData);

                    // Обновление UI
                    string inputDataDescription = GetInputDataDescription(inputData);
                    InputDataTextBlock.Text = inputDataDescription;

                    // Построение графика
                    var plotModel = CreatePlotModel(_currentResult);
                    MainPlotView.Model = plotModel;

                    // Сообщение об успехе
                    StatusTextBlock.Text = "Расчет успешно выполнен!";

                    // Добавление команды в менеджер Undo/Redo
                    _undoManager.AddUndoRedo(
                        // Undo Action
                        () =>
                        {
                            _currentInputData = previousInput;
                            _currentResult = previousResult;
                            InputDataTextBlock.Text = previousText;
                            MainPlotView.Model = previousModel;
                            StatusTextBlock.Text = "Действие отменено";
                        },
                        // Redo Action
                        () =>
                        {
                            _currentInputData = inputData;
                            _currentResult = _currentResult;
                            InputDataTextBlock.Text = inputDataDescription;
                            MainPlotView.Model = plotModel;
                            StatusTextBlock.Text = "Действие возвращено";
                        }
                    );
                }
                catch (Exception ex)
                {
                    MessageBox.Show($"Ошибка: {ex.Message}", "Ошибка выполнения", MessageBoxButton.OK, MessageBoxImage.Error);
                    StatusTextBlock.Text = "Ошибка выполнения";
                    StatusTextBlock.Foreground = System.Windows.Media.Brushes.Red;
                }
            }

            private InputData ParseFile(string path)
            {
                if (!System.IO.File.Exists(path))
                    throw new System.IO.FileNotFoundException("Файл не найден", path);

                string content = System.IO.File.ReadAllText(path).ToLower();

                ParserBase parser = content.Contains("mass") || content.Contains("stiffness")
                    ? new OscillatorParser(path)
                    : (content.Contains("resistance") || content.Contains("capacitance")
                        ? new RcParser(path)
                        : new CoolingParser(path));

                return parser.Parse();
            }

            private string GetInputDataDescription(InputData data)
            {
                return data switch
                {
                    OscillatorInput o => $"Тип: Маятник\n" +
                                         $"Масса: {o.Mass} кг\n" +
                                         $"Жесткость: {o.Stiffness} Н/м\n" +
                                         $"Затухание: {o.Damping} кг/с\n" +
                                         $"X0: {o.X0} м\n" +
                                         $"V0: {o.V0} м/с\n" +
                                         $"Время: {o.MaxTime} с\n" +
                                         $"Шаг: {o.DeltaT} с",

                    RCInput r => $"Тип: RC Цепь\n" +
                                 $"Сопротивление: {r.Resistance} Ом\n" +
                                 $"Ёмкость: {r.Capacitance} Ф\n" +
                                 $"Напряжение источника: {r.VoltageSource} В\n" +
                                 $"Начальное напряжение: {r.U0} В\n" +
                                 $"Время: {r.MaxTime} с\n" +
                                 $"Шаг: {r.DeltaT} с",

                    CoolingInput c => $"Тип: Охлаждение\n" +
                                      $"Начальная температура: {c.T0} °C\n" +
                                      $"Температура среды: {c.Tenv} °C\n" +
                                      $"Коэффициент: {c.Coeff} 1/с\n" +
                                      $"Время: {c.MaxTime} с\n" +
                                      $"Шаг: {c.DeltaT} с",
                    _ => "Неизвестный тип данных"
                };
            }

            private PlotModel CreatePlotModel(SolverResult result)
            {
                var plotModel = new PlotModel { Title = result.Title };
                var series = new LineSeries();

                int minLength = Math.Min(result.XValues.Length, result.YValues.Length);
                for (int i = 0; i < minLength; i++)
                {
                    series.Points.Add(new DataPoint(result.XValues[i], result.YValues[i]));
                }

                plotModel.Series.Add(series);
                return plotModel;
            }

            private void UndoButton_Click(object sender, RoutedEventArgs e)
            {
                _undoManager.Undo();
            }

            private void RedoButton_Click(object sender, RoutedEventArgs e)
            {
                _undoManager.Redo();
            }
        }
}