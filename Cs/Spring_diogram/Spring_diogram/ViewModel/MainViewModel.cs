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
            UndoCommand = new RelayCommand(_ => Undo());
            RedoCommand = new RelayCommand(_ => Redo());
        }

        public InputViewModel InputViewModel { get; }
        public SolverViewModel SolverViewModel { get; }

        public System.Windows.Input.ICommand UndoCommand { get; }
        public System.Windows.Input.ICommand RedoCommand { get; }

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
