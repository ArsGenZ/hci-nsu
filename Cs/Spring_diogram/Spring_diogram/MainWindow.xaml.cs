using System.Windows;
using Spring_diogram.ViewModel;

namespace Spring_diogram
{
    public partial class MainWindow : Window
    {
        private MainViewModel _mainViewModel;

        public MainWindow()
        {
            _mainViewModel = new MainViewModel();
            DataContext = _mainViewModel;

            InitializeComponent();
        }

        private void BrowseButton_Click(object sender, RoutedEventArgs e)
        {
            _mainViewModel.InputViewModel.SelectFile();
        }

        private void LoadButton_Click(object sender, RoutedEventArgs e)
        {
            try
            {
                _mainViewModel.InputViewModel.LoadDataFromFile();
                _mainViewModel.SolverViewModel.Solve();
                StatusTextBlock.Text = "Расчет успешно выполнен!";
            }
            catch (System.Exception ex)
            {
                MessageBox.Show($"Ошибка: {ex.Message}", "Ошибка выполнения", MessageBoxButton.OK, MessageBoxImage.Error);
                StatusTextBlock.Text = "Ошибка выполнения";
                StatusTextBlock.Foreground = System.Windows.Media.Brushes.Red;
            }
        }

        private void UndoButton_Click(object sender, RoutedEventArgs e)
        {
            _mainViewModel.Undo();
        }

        private void RedoButton_Click(object sender, RoutedEventArgs e)
        {
            _mainViewModel.Redo();
        }
    }
}