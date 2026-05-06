using Spring_diogram.DATA;
using System.Globalization;
using System.IO;

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
                var reader = new StreamReader(_fileStream);
                string[] lines = File.ReadAllLines(_path);

                foreach (string line in lines)
                {
                    string trimmedLine = line.Trim();

                    if (string.IsNullOrEmpty(trimmedLine) || trimmedLine.StartsWith("#"))
                        continue;

                    int equalsIndex = trimmedLine.IndexOf(',');
                    if (equalsIndex == -1)
                        equalsIndex = trimmedLine.IndexOf("=");
                    if (equalsIndex == -1)
                        equalsIndex = trimmedLine.IndexOf(":");
                    if (equalsIndex == -1)
                        continue;

                    string key = trimmedLine.Substring(0, equalsIndex).Trim().ToLower();
                    string value = trimmedLine.Substring(equalsIndex + 1).Trim();

                    if (double.TryParse(value, NumberStyles.Any, CultureInfo.InvariantCulture, out double numericValue))
                    {
                        switch (key)
                        {
                            case "t0":
                                input.T0 = numericValue;
                                break;
                            case "tenv":
                                input.Tenv = numericValue;
                                break;
                            case "coeff":
                                input.Coeff = numericValue;
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

                input.Name = "Cooling";
                return input;
            }
            catch (Exception ex)
            {
                throw new Exception($"Ошибка парсинга файла охлаждения: {ex.Message}", ex);
            }
        }
    }
}
