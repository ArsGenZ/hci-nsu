namespace Spring_diogram.Common
{
    public class UndoRedoCommand
    {
        private readonly Action _undoAction;
        private readonly Action _redoAction;

        public UndoRedoCommand(Action undoAction, Action redoAction)
        {
            _undoAction = undoAction;
            _redoAction = redoAction;
        }

        public void Undo() => _undoAction();
        public void Redo() => _redoAction();
    }
}
