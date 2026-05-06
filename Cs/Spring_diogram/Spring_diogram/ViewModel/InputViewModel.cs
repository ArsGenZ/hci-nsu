using Spring_diogram.Common;
using Spring_diogram.DATA;
using Microsoft.Win32;

namespace Spring_diogram.ViewModel
{
    public class InputViewModel : ViewModelBase
    {
        private readonly UndoRedoManager _undoRedoManager;
        private string _filePath = "";
        private InputData? _currentImportedData;

        public InputViewModel(UndoRedoManager undoRedoManager)
        {
            _undoRedoManager = undoRedoManager;
        }

        public string FilePath
        {
            get => _filePath;
            set
            {
                if (_filePath != value)
                {
                    var oldValue = _filePath;
                    _filePath = value;
                    OnPropertyChanged();
                    _undoRedoManager.AddUndoRedo(
                        () => { _filePath = oldValue; OnPropertyChanged(nameof(FilePath)); },
                        () => { _filePath = value; OnPropertyChanged(nameof(FilePath)); }
                    );
                }
            }
        }

        public InputData? CurrentImportedData
        {
            get => _currentImportedData;
            set
            {
                if (_currentImportedData != value)
                {
                    var oldValue = _currentImportedData;
                    _currentImportedData = value;
                    OnPropertyChanged();
                    OnPropertyChanged(nameof(InputDataDescription));
                    _undoRedoManager.AddUndoRedo(
                        () => { _currentImportedData = oldValue; OnPropertyChanged(nameof(CurrentImportedData)); OnPropertyChanged(nameof(InputDataDescription)); },
                        () => { _currentImportedData = value; OnPropertyChanged(nameof(CurrentImportedData)); OnPropertyChanged(nameof(InputDataDescription)); }
                    );
                }
            }
        }

        public string InputDataDescription => CurrentImportedData?.ToString() ?? "";

        public void SelectFile()
        {
            OpenFileDialog openFileDialog = new OpenFileDialog
            {
                Filter = "Text files|*.txt;*.xml;*.json|All files|*.*",
                Title = "Выберите файл входных данных"
            };

            if (openFileDialog.ShowDialog() == true)
            {
                FilePath = openFileDialog.FileName;
            }
        }

        public void LoadDataFromFile()
        {
            if (string.IsNullOrEmpty(FilePath))
                throw new System.Exception("Путь к файлу не указан!");

            InputData inputData = ParseFile(FilePath);
            CurrentImportedData = inputData;
        }

        private InputData ParseFile(string path)
        {
            if (!System.IO.File.Exists(path))
                throw new System.IO.FileNotFoundException("Файл не найден", path);

            string content = System.IO.File.ReadAllText(path).ToLower();

            ParserBase parser = content.Contains("mass") || content.Contains("stiffness")
                ? new Parsers.OscillatorParser(path)
                : (content.Contains("resistance") || content.Contains("capacitance")
                    ? new Parsers.RcParser(path)
                    : new Parsers.CoolingParser(path));

            return parser.Parse();
        }
    }
}
