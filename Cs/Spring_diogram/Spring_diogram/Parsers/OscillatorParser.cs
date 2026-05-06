using Spring_diogram.DATA;
using System.Globalization;
using System.IO;

namespace Spring_diogram.Parsers
{
    public class OscillatorParser : ParserBase
    {
        public OscillatorParser(string path) : base(path) { }

        public override InputData Parse()
        {
            var input = new OscillatorInput();

            try
            {
                string[] lines = File.ReadAllLines(_path);

                foreach (string line in lines)
                {
                    string trimmedLine = line.Trim();

                    // Пропускаем пустые строки и комментарии
                    if (string.IsNullOrEmpty(trimmedLine) || trimmedLine.StartsWith("#"))
                        continue;

                    // Ищем знак разделения ключа и значения
                    int equalsIndex = trimmedLine.IndexOf(',');
                    if (equalsIndex == -1)
                        equalsIndex = trimmedLine.IndexOf("=");
                    if (equalsIndex == -1)
                        equalsIndex = trimmedLine.IndexOf(":");
                    if (equalsIndex == -1)
                        continue;


                    string key = trimmedLine.Substring(0, equalsIndex).Trim().ToLower();
                    string value = trimmedLine.Substring(equalsIndex + 1).Trim();

                    // Парсим число с invariant culture (точка как разделитель)
                    if (double.TryParse(value, NumberStyles.Any, CultureInfo.InvariantCulture, out double numericValue))
                    {
                        switch (key)
                        {
                            case "mass":
                                input.Mass = numericValue;
                                break;
                            case "stiffness":
                                input.Stiffness = numericValue;
                                break;
                            case "damping":
                                input.Damping = numericValue;
                                break;
                            case "x0":
                                input.X0 = numericValue;
                                break;
                            case "v0":
                                input.V0 = numericValue;
                                break;
                            case "timemax":
                                input.MaxTime = numericValue;
                                break;
                            case "timestep":
                                input.DeltaT = numericValue;
                                break;
                        }
                    }
                }

                input.Name = "Oscillator";
                return input;
            }
            catch (Exception ex)
            {
                throw new Exception($"Ошибка парсинга файла осциллятора: {ex.Message}", ex);
            }
        }
    }
}
