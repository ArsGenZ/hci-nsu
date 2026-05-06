using Spring_diogram.DATA;
using System.IO;

namespace Spring_diogram.Parsers
{
    public abstract class ParserBase
    {
        protected readonly FileStream _fileStream;
        protected readonly string _path;

        protected ParserBase(string path)
        {
            _path = path;
            if (!File.Exists(path))
                throw new FileNotFoundException("Файл не найден", path);

            _fileStream = File.OpenRead(path);
        }

        public abstract InputData Parse();
    }
}

