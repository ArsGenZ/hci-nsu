using Spring_diogram.Common;

namespace Spring_diogram.ViewModel
{
    public class MainViewModel : ViewModelBase
    {
        private readonly UndoRedoManager _undoRedoManager;

        public MainViewModel()
        {
            _undoRedoManager = new UndoRedoManager();
            InputViewModel = new InputViewModel(_undoRedoManager);
            SolverViewModel = new SolverViewModel(_undoRedoManager, InputViewModel);
            InputViewModel.SolverViewModel = SolverViewModel;
            _undoRedoManager.HistoryChanged += OnHistoryChanged;
            UndoCommand = new RelayCommand(_ => Undo(), CanUndo);
            RedoCommand = new RelayCommand(_ => Redo(), CanRedo);
        }

        public InputViewModel InputViewModel { get; }
        public SolverViewModel SolverViewModel { get; }

        public System.Windows.Input.ICommand UndoCommand { get; }
        public System.Windows.Input.ICommand RedoCommand { get; }

        private void OnHistoryChanged()
        {
            ((RelayCommand)UndoCommand).RaiseCanExecuteChanged();
            ((RelayCommand)RedoCommand).RaiseCanExecuteChanged();
        }

        private bool CanUndo(object parameter) => _undoRedoManager.CanUndo;
        private bool CanRedo(object parameter) => _undoRedoManager.CanRedo;

        public void Undo()
        {
            _undoRedoManager.Undo();
        }

        public void Redo()
        {
            _undoRedoManager.Redo();
        }
    }
}
