using Spring_diogram.DATA;
using System.Globalization;
using System.IO;
using System.Xml.Linq;

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
                
                // Пропускаем первую строку (название "oscillator")
                for (int i = 1; i < lines.Length; i++)
                {
                    string trimmedLine = lines[i].Trim();

                    // Пропускаем пустые строки и комментарии
                    if (string.IsNullOrEmpty(trimmedLine) || trimmedLine.StartsWith("#"))
                        continue;

                    // Формат TXT: key=value или key:value через запятую
                    int separatorIndex = trimmedLine.IndexOf('=');
                    if (separatorIndex == -1)
                        separatorIndex = trimmedLine.IndexOf(':');
                    if (separatorIndex == -1)
                        separatorIndex = trimmedLine.IndexOf(',');
                    if (separatorIndex == -1)
                        continue;

                    string key = trimmedLine.Substring(0, separatorIndex).Trim().ToLower();
                    string value = trimmedLine.Substring(separatorIndex + 1).Trim();

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
                throw new Exception($"Ошибка парсинга файла осциллятора (TXT): {ex.Message}", ex);
            }
        }
    }
}
