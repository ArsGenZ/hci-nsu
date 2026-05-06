namespace Spring_diogram.Common
{
    public class UndoRedoManager
    {
        private readonly Stack<UndoRedoCommand> _undoStack = new();
        private readonly Stack<UndoRedoCommand> _redoStack = new();

        public void AddUndoRedo(Action undoAction, Action redoAction)
        {
            var command = new UndoRedoCommand(undoAction, redoAction);
            _undoStack.Push(command);
            _redoStack.Clear();
        }

        public void Undo()
        {
            if (_undoStack.Count > 0)
            {
                var command = _undoStack.Pop();
                command.Undo();
                _redoStack.Push(command);
            }
        }

        public void Redo()
        {
            if (_redoStack.Count > 0)
            {
                var command = _redoStack.Pop();
                command.Redo();
                _undoStack.Push(command);
            }
        }
    }
}
