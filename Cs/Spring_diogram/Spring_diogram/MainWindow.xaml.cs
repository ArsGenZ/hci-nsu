using System.Windows;
using Spring_diogram.ViewModel;

namespace Spring_diogram
{
    public partial class MainWindow : Window
    {
        public MainWindow()
        {
            InitializeComponent();
            DataContext = new MainViewModel();
        }
    }
}