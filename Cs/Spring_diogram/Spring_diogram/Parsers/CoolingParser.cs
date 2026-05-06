using Spring_diogram.DATA;
using System.Globalization;
using System.IO;
using System.Xml.Linq;

namespace Spring_diogram.Parsers
{
    public class CoolingParser : ParserBase
    {
        public CoolingParser(string path) : base(path) { }

        public override InputData Parse()
        {
            var input = new CoolingInput();

            try
            {
                // Чтение всех строк и пропуск первой строки (название)
                string[] lines = File.ReadAllLines(_path);
                if (lines.Length == 0)
                    throw new Exception("XML файл пуст");

                // Пропускаем первую строку (название "cooling")
                string xmlContent = string.Join(Environment.NewLine, lines.Skip(1));
                
                // Парсинг XML формата
                XDocument doc = XDocument.Parse(xmlContent);
                XElement root = doc.Root;

                if (root == null)
                    throw new Exception("XML файл пуст или некорректен");

                // Чтение элементов XML
                XElement t0Elem = root.Element("T0") ?? root.Element("t0");
                if (t0Elem != null && double.TryParse(t0Elem.Value, NumberStyles.Any, CultureInfo.InvariantCulture, out double t0))
                    input.T0 = t0;

                XElement tenvElem = root.Element("Tenv") ?? root.Element("tenv");
                if (tenvElem != null && double.TryParse(tenvElem.Value, NumberStyles.Any, CultureInfo.InvariantCulture, out double tenv))
                    input.Tenv = tenv;

                XElement coeffElem = root.Element("Coeff") ?? root.Element("coeff");
                if (coeffElem != null && double.TryParse(coeffElem.Value, NumberStyles.Any, CultureInfo.InvariantCulture, out double coeff))
                    input.Coeff = coeff;

                XElement timeMaxElem = root.Element("TimeMax") ?? root.Element("timemax");
                if (timeMaxElem != null && double.TryParse(timeMaxElem.Value, NumberStyles.Any, CultureInfo.InvariantCulture, out double timeMax))
                    input.MaxTime = timeMax;

                XElement timeStepElem = root.Element("TimeStep") ?? root.Element("timestep");
                if (timeStepElem != null && double.TryParse(timeStepElem.Value, NumberStyles.Any, CultureInfo.InvariantCulture, out double timeStep))
                    input.DeltaT = timeStep;

                input.Name = "Cooling";
                return input;
            }
            catch (Exception ex)
            {
                throw new Exception($"Ошибка парсинга файла охлаждения (XML): {ex.Message}", ex);
            }
        }
    }
}
