using Spring_diogram.DATA;
using System.Globalization;
using System.IO;

namespace Spring_diogram.Parsers
{
    public class RcParser : ParserBase
    {
        public RcParser(string path) : base(path) { }

        public override InputData Parse()
        {
            var input = new RCInput();

            try
            {
                string[] lines = File.ReadAllLines(_path);

                foreach (string line in lines)
                {
                    string trimmedLine = line.Trim();

                    if (string.IsNullOrEmpty(trimmedLine))
                        continue;

                    int equalsIndex = trimmedLine.IndexOf(',');
                    if (equalsIndex == -1)
                        continue;

                    string key = trimmedLine.Substring(0, equalsIndex).Trim().ToLower();
                    string value = trimmedLine.Substring(equalsIndex + 1).Trim();

                    if (double.TryParse(value, NumberStyles.Any, CultureInfo.InvariantCulture, out double numericValue))
                    {
                        switch (key)
                        {
                            case "resistance":
                                input.Resistance = numericValue;
                                break;
                            case "capacitance":
                                input.Capacitance = numericValue;
                                break;
                            case "voltagesource":
                                input.VoltageSource = numericValue;
                                break;
                            case "u0":
                                input.U0 = numericValue;
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

                input.Name = "RC Circuit";
                return input;
            }
            catch (Exception ex)
            {
                throw new Exception($"Ошибка парсинга RC файла: {ex.Message}", ex);
            }
        }
    }
}

